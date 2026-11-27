import type { APIRequestContext, Page } from '@playwright/test';
import { API_ENDPOINTS, ROUTES, expect } from './strict-fixtures';

export const ROUTINE_A = 'GYM - Full Body - Workout A';
export const ROUTINE_B = 'GYM - Full Body - Workout B';
const LONG_ROUTINE = 'GYM - Upper Lower Hypertrophy Split - Workout B Heavy';

export const SQUAT = 'Barbell Squat';
export const DEADLIFT = 'Barbell Deadlift';
export const BENCH = 'Barbell Bench Press';
export const ROW = 'Barbell Bent Over Row';
const CURL = 'Barbell Curl';
const PRESS = 'Barbell Seated Military Press';
export const LONG_EXERCISE = 'Cable Standing Single Arm Internally Rotated Incline Chest Fly';
export const SQUAT_FIELDS = { sets: 10, min_rep_range: 30, max_rep_range: 30, weight: 102.5, rir: 10, rpe: 9.5 };

export type PlanRow = {
  id: number;
  routine: string;
  exercise: string;
  sets: number;
  min_rep_range: number;
  max_rep_range: number;
  weight: number;
  rir: number;
  rpe: number | null;
  exercise_order: number;
  superset_group: string | null;
  execution_style: string;
  time_cap_seconds: number | null;
};

export const planRows = (page: Page) => page.locator('#workout_plan_table_body tr[data-exercise-id]');
export const planRow = (page: Page, id: number) => planRows(page).and(page.locator('[data-exercise-id="' + id + '"]'));
export const routineTab = (page: Page, routine: string) =>
  page.locator('#routine-tabs button[data-routine="' + routine + '"]');
export const details = (page: Page, id: number) => planRow(page, id).getByRole('button', { name: 'Details', exact: true });

export async function planData(request: APIRequestContext): Promise<PlanRow[]> {
  const response = await request.get(API_ENDPOINTS.GET_WORKOUT_PLAN);
  const body = await response.json();
  expect(response.status(), API_ENDPOINTS.GET_WORKOUT_PLAN).toBe(200);
  expect(body.ok, API_ENDPOINTS.GET_WORKOUT_PLAN).toBe(true);
  return body.data;
}

export async function planPost(request: APIRequestContext, endpoint: string, data?: object) {
  const response = await request.post(endpoint, { data });
  const body = await response.json();
  expect(response.status(), endpoint + ': ' + JSON.stringify(body)).toBe(200);
  expect(body.ok, endpoint).toBe(true);
  return body;
}

export async function addPlanRow(
  request: APIRequestContext, routine: string, exercise: string, fields: Partial<PlanRow> = {},
) {
  await planPost(request, API_ENDPOINTS.ADD_EXERCISE, {
    routine, exercise, sets: 3, min_rep_range: 6, max_rep_range: 10, weight: 50, rir: 2, ...fields,
  });
}

export async function loadPlan(page: Page, reload = false) {
  const checked = page.waitForResponse(response =>
    new URL(response.url()).pathname === API_ENDPOINTS.GET_WORKOUT_PLAN && response.request().method() === 'GET',
  );
  if (reload) await page.reload();
  else await page.goto(ROUTES.WORKOUT_PLAN);
  const response = await checked;
  expect(response.status()).toBe(200);
  expect((await response.json()).ok).toBe(true);
  await page.locator('#tab-all .tab-count').filter({ hasText: /\d/ }).waitFor();
}

export async function addTheWidePhoneValues(request: APIRequestContext) {
  await addPlanRow(request, ROUTINE_A, SQUAT, SQUAT_FIELDS);
  await addPlanRow(request, ROUTINE_A, DEADLIFT, { weight: 999.5 });
  const entries = await planData(request);
  const squat = entries.find(entry => entry.exercise === SQUAT);
  const deadlift = entries.find(entry => entry.exercise === DEADLIFT);
  expect(squat).toMatchObject(SQUAT_FIELDS);
  expect(deadlift).toMatchObject({ weight: 999.5 });
  return { squat: squat!, deadlift: deadlift! };
}

/** Edit the checked-in six-row visual seed through the same routes as the page. */
export async function editVisualPlanFixture(request: APIRequestContext): Promise<PlanRow[]> {
  const seed = await planData(request);
  expect(seed.map(row => [row.routine, row.exercise])).toEqual(
    [BENCH, ROW, SQUAT, DEADLIFT, CURL, PRESS].map(exercise => [ROUTINE_A, exercise]),
  );
  const byName = Object.fromEntries(seed.map(row => [row.exercise, row.id]));

  await planPost(request, API_ENDPOINTS.SUPERSET_LINK, { exercise_ids: [byName[BENCH], byName[ROW]] });
  await planPost(request, API_ENDPOINTS.UPDATE_EXERCISE, { id: byName[SQUAT], updates: SQUAT_FIELDS });
  await planPost(request, API_ENDPOINTS.UPDATE_EXERCISE, { id: byName[DEADLIFT], updates: { weight: 999.5 } });
  await planPost(request, '/api/execution_style', {
    exercise_id: byName[CURL], execution_style: 'amrap', time_cap_seconds: 60,
  });
  const additions = [
    { routine: ROUTINE_A, exercise: LONG_EXERCISE, sets: 3, min_rep_range: 12, max_rep_range: 15, weight: 12.5 },
    { routine: ROUTINE_B, exercise: BENCH, sets: 4, min_rep_range: 6, max_rep_range: 10, weight: 50 },
    { routine: ROUTINE_B, exercise: DEADLIFT, sets: 3, min_rep_range: 8, max_rep_range: 12, weight: 90 },
    { routine: LONG_ROUTINE, exercise: ROW, sets: 3, min_rep_range: 10, max_rep_range: 12, weight: 55 },
  ];
  for (const { routine, exercise, ...fields } of additions) {
    await addPlanRow(request, routine, exercise, fields);
  }

  const rows = await planData(request);
  expect(rows).toHaveLength(10);
  const group = rows[0].superset_group;
  expect(group).toBeTruthy();
  expect(rows).toMatchObject([
    { ...seed[0], superset_group: group },
    { ...seed[1], superset_group: group },
    { ...seed[2], ...SQUAT_FIELDS },
    { ...seed[3], weight: 999.5 },
    { ...seed[4], execution_style: 'amrap', time_cap_seconds: 60 },
    seed[5],
    ...additions.map((row, index) => ({
      ...row, rir: 2, rpe: null, exercise_order: index + 7, execution_style: 'standard', superset_group: null,
    })),
  ]);
  return rows;
}
