import { fetchWeeklySummary, fetchSessionSummary } from './summary.js';
import { handleDateChange, isScoredRepField, saveEditedScore, validateScoredValue } from './workout-log.js';
import { showToast } from './toast.js';

/**
 * Add custom +/- buttons to number inputs for reliable increment/decrement
 * Native browser spinners can be unreliable across different browsers/platforms
 */
function addCustomSpinnerButtons(input) {
    // Don't add buttons if already added
    if (input.dataset.hasCustomSpinners === 'true') return;
    input.dataset.hasCustomSpinners = 'true';
    
    // Create wrapper for the input + buttons
    const wrapper = document.createElement('div');
    wrapper.className = 'number-input-wrapper';
    // Start hidden; the edit-click handler switches to inline-flex when the user opens the editor
    wrapper.style.cssText = 'display: none; align-items: center; gap: 2px;';
    
    // Insert wrapper in place of input
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);
    
    // Create minus button
    const minusBtn = document.createElement('button');
    minusBtn.type = 'button';
    minusBtn.setAttribute('aria-label', 'Decrease ' + input.getAttribute('aria-label'));
    minusBtn.className = 'number-spinner-btn number-spinner-minus';
    minusBtn.innerHTML = '−'; // Use Unicode minus for better click area
    minusBtn.style.cssText = `
        width: 26px; height: 26px; padding: 0; border: 1px solid #ccc;
        background: #f8f9fa; border-radius: 4px; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; font-weight: bold; color: #495057; line-height: 1;
        user-select: none;
    `;
    
    // Create plus button
    const plusBtn = document.createElement('button');
    plusBtn.type = 'button';
    plusBtn.setAttribute('aria-label', 'Increase ' + input.getAttribute('aria-label'));
    plusBtn.className = 'number-spinner-btn number-spinner-plus';
    plusBtn.innerHTML = '+'; // Use plain text for better click area
    plusBtn.style.cssText = minusBtn.style.cssText;
    
    // Insert buttons
    wrapper.insertBefore(minusBtn, input);
    wrapper.appendChild(plusBtn);
    
    // Get step from input or default to 1
    const step = parseFloat(input.step) || 1;
    // Default min to 0 to prevent negative numbers for workout data
    const min = input.min !== '' ? parseFloat(input.min) : 0;
    const max = input.max !== '' ? parseFloat(input.max) : null;
    
    // Set min attribute on input if not already set
    if (!input.hasAttribute('min')) {
        input.setAttribute('min', '0');
    }
    
    // Handler to change value
    function changeValue(delta) {
        let currentValue = parseFloat(input.value) || 0;
        let newValue = currentValue + delta;
        
        // Respect min/max - always prevent negative
        if (newValue < min) newValue = min;
        if (max !== null && newValue > max) newValue = max;
        
        input.value = newValue;
        
        // Trigger input and change events so handlers respond
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Keep input focused
        input.focus();
    }
    
    // Add click handlers
    minusBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        changeValue(-step);
    });
    
    plusBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        changeValue(step);
    });
    
    // Prevent blur when clicking buttons
    minusBtn.addEventListener('mousedown', (e) => e.preventDefault());
    plusBtn.addEventListener('mousedown', (e) => e.preventDefault());
}

export function initializeUIHandlers() {
    let activeScoreEditor = null;

    function confirmedScore(cell) {
        const displayed = cell.querySelector('.editable-text').textContent.trim();
        return displayed === '--' ? '' : displayed;
    }

    function initializeScoreEditor(input, cell, field) {
        const logId = cell.closest('tr[data-log-id]').dataset.logId;
        const wrapper = input.closest('.number-input-wrapper');
        let edited = false;
        const editor = { cell, finish };

        async function finish(save, restoreFocus = false) {
            if (activeScoreEditor !== editor) return;
            activeScoreEditor = null;

            const value = input.value;
            const valid = !input.validity.badInput && validateScoredValue(value, field);
            const changed = save && edited;
            const submit = changed && valid && value !== confirmedScore(cell);
            edited = false;
            input.classList.remove('is-invalid', 'is-valid');
            if (submit) input.disabled = true;
            input.style.display = 'none';
            wrapper.style.display = 'none';
            const trigger = cell.querySelector('.log-trigger, .editable-text');
            trigger.style.display = '';

            if (changed && !valid) {
                const message = isScoredRepField(field)
                    ? 'Scored reps must be a whole number of at least 0.'
                    : `Enter a number from ${input.min} to ${input.max} for ${cell.dataset.label}.`;
                showToast('warning', message);
            }
            if (restoreFocus) trigger.focus();
            if (submit) {
                try {
                    await saveEditedScore(logId, field, value);
                } finally {
                    input.disabled = false;
                }
                if (restoreFocus && !trigger.getClientRects().length && document.activeElement === document.body) {
                    cell.closest('tr').querySelector('.log-details')?.focus();
                }
            }
        }

        // Keep drafts local until the editor closes. The API updates the visible
        // value only after confirming the save, so Escape and rejection leave it intact.
        input.addEventListener('focus', () => { activeScoreEditor = editor; });
        input.addEventListener('input', () => {
            edited = true;
            const valid = !input.validity.badInput && validateScoredValue(input.value, field);
            input.classList.toggle('is-invalid', !valid);
            input.classList.toggle('is-valid', valid);
        });
        wrapper.addEventListener('focusout', (event) => {
            if (!wrapper.contains(event.relatedTarget)) void finish(true);
        });
        wrapper.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' || (event.key === 'Enter' && event.target === input)) {
                event.preventDefault();
                void finish(event.key === 'Enter', true);
            }
        });
    }

    // Handle editable fields
    document.querySelectorAll('.editable').forEach(cell => {
        cell.addEventListener('click', function(e) {
            // Don't trigger if clicking on the input or spinner buttons
            if (e.target.classList.contains('editable-input') || 
                e.target.classList.contains('number-spinner-btn') ||
                e.target.closest('.number-spinner-btn')) {
                return;
            }
            
            const input = this.querySelector('.editable-input');
            const text = this.querySelector('.log-trigger, .editable-text');
            const wrapper = this.querySelector('.number-input-wrapper');
            
            if (input) {
                if (this.classList.contains('scored-cell')) {
                    if (input.disabled || input.style.display !== 'none') return;
                    input.value = confirmedScore(this);
                }
                text.style.display = 'none';
                input.style.display = 'block';
                // Also show the wrapper if it exists (for number inputs with custom buttons)
                if (wrapper) {
                    wrapper.style.display = 'inline-flex';
                }
                input.focus();
                
                // For date inputs, open the picker immediately
                if (input.type === 'date' && typeof input.showPicker === 'function') {
                    try {
                        input.showPicker();
                    } catch (err) {
                        // Silently fail if not supported
                    }
                }
            }
        });
    });
    
    // Initialize date input change handlers
    document.querySelectorAll('.date-editable .date-input').forEach(input => {
        input.addEventListener('change', function() {
            const logId = this.dataset.logId;
            if (logId) {
                handleDateChange({ target: this }, logId);
            }
        });
    });

    // Handle clicking outside editable fields
    document.addEventListener('click', function(e) {
        // Don't hide if clicking on spinner buttons
        if (e.target.classList.contains('number-spinner-btn') || 
            e.target.closest('.number-spinner-btn')) {
            return;
        }
        if (activeScoreEditor && !activeScoreEditor.cell.contains(e.target)) {
            void activeScoreEditor.finish(true);
        }
        
        if (!e.target.closest('.editable') && !e.target.classList.contains('editable-input')) {
            document.querySelectorAll('.editable-input').forEach(input => {
                input.style.display = 'none';
            });
            document.querySelectorAll('.log-trigger, .editable-text:not(.log-trigger .editable-text)').forEach(text => {
                // Use flex for date displays, block for others
                text.style.display = text.classList.contains('log-trigger') ? '' : text.classList.contains('date-display') ? 'flex' : 'block';
            });
            // Also hide number input wrappers
            document.querySelectorAll('.number-input-wrapper').forEach(wrapper => {
                wrapper.style.display = 'none';
            });
        }
    });

    // Handle routine dropdown click state
    const routineDropdown = document.querySelector('.routine-dropdown');
    if (routineDropdown) {
        routineDropdown.addEventListener('click', function() {
            this.classList.add('clicked');
        });

        // Reset background when clicking outside
        document.addEventListener('click', function(event) {
            if (!routineDropdown.contains(event.target)) {
                routineDropdown.classList.remove('clicked');
            }
        });
    }

    initializeSummaryMethodHandlers();

    document.querySelectorAll('tr[data-log-id] .scored-cell input[type="number"]').forEach(input => {
        const cell = input.closest('.scored-cell');
        addCustomSpinnerButtons(input);
        initializeScoreEditor(input, cell, cell.dataset.field);
    });
}

export function initializeFormHandlers() {
    // Add Exercise button handler
    const addExerciseBtn = document.getElementById('add-exercise-btn');
    if (addExerciseBtn) {
        addExerciseBtn.addEventListener('click', () => {
            console.log('Add Exercise button clicked');
            // The actual addExercise function will be imported where needed
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

export function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

export function initializeDropdowns() {
    // Initialize all dropdowns
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        new bootstrap.Dropdown(dropdown);
    });
}

export function handleTableSort() {
    document.querySelectorAll('th[data-sort]').forEach(header => {
        header.addEventListener('click', () => {
            const table = header.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const column = header.dataset.sort;
            const ascending = header.classList.toggle('sort-asc');

            const sortedRows = rows.sort((a, b) => {
                const aValue = a.querySelector(`td[data-${column}]`)?.textContent;
                const bValue = b.querySelector(`td[data-${column}]`)?.textContent;
                return ascending ? 
                    aValue.localeCompare(bValue) : 
                    bValue.localeCompare(aValue);
            });

            tbody.innerHTML = '';
            sortedRows.forEach(row => tbody.appendChild(row));
        });
    });
}

function initializeSummaryMethodHandlers() {
    const methodSelect = document.getElementById('summary-method');
    if (!methodSelect) return;

    methodSelect.addEventListener('change', (e) => {
        const method = e.target.value;
        const currentPath = window.location.pathname;
        
        if (currentPath === '/weekly_summary') {
            fetchWeeklySummary(method);
        } else if (currentPath === '/session_summary') {
            fetchSessionSummary(method);
        }
    });
}

function initializeSuggestionCards() {
    document.querySelectorAll('.suggestion-card').forEach(card => {
        const toggle = card.querySelector('.expand-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => {
                card.classList.toggle('expanded');
                toggle.textContent = card.classList.contains('expanded') ? 'Show Less' : 'Show More';
            });
        }
    });
}

// Call this function when suggestions are loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeSuggestionCards();
}); 
