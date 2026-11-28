export class ApiError extends Error {
  constructor(public status: number, public body: Record<string, unknown>) {
    super(typeof body.detail === 'string' ? body.detail : String(status));
  }
}

export async function api<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  const token = document.cookie.split('; ').find((cookie) => cookie.startsWith('csrftoken='))?.slice(10);
  const response = await fetch('/api' + path, {
    method,
    headers: {
      ...(token ? { 'X-CSRFToken': token } : {}),
      ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: 'no-store',
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(response.status, result);
  return result as T;
}

export type Translate = (fa: string, en: string) => string;
export type User = { id: string; email: string };
export type Workspace = { id: string; name: string; currency: string; timezone: string; role: string };
export type Method = {
  tool_id: string; method_id: string; method_version: number; quick: boolean;
  availability: string; required_for_primary: string[]; release_gate: string;
};
export type Ref = { kind: string; id: string; version: number };
export type RunRequest = {
  workspace_id: string; tool_id: string; method_id: string; method_version: number;
  question: string; input: Record<string, unknown>; evidence_refs: Ref[];
  dependency_run_ids: string[]; idempotency_key: string;
};
export type Draft = { id: string; version: number; series: string; request: RunRequest };

export function errorText(error: unknown, t: Translate) {
  if (!(error instanceof ApiError)) return t('ارتباط برقرار نشد. دوباره تلاش کنید.', 'Could not connect. Please try again.');
  if (error.body.code === 'csrf_failed') return t('نشست منقضی شده است. صفحه را تازه کنید.', 'Session expired. Refresh the page.');
  if (error.status === 401) return t('ورود ناموفق بود یا نشست پایان یافته است.', 'Sign-in failed or the session expired.');
  if (error.status === 403) return t('مجوز این کار را ندارید.', 'You do not have permission for this action.');
  if (error.status === 404) return t('این مورد در فضای کاری در دسترس نیست.', 'This item is unavailable in this workspace.');
  if (error.status === 409) return t('نسخه تغییر کرده یا کلید درخواست تکراری است.', 'The version changed or the request key conflicts.');
  if (error.status === 429) return t('تعداد درخواست‌ها زیاد است. کمی بعد دوباره تلاش کنید.', 'Too many requests. Try again later.');
  if (error.status === 503) return t('این روش در برنامهٔ توسعه است.', 'This method is planned.');
  const fields = error.body.fields;
  const detail = fields && typeof fields === 'object'
    ? Object.entries(fields).map(([key, value]) => key + ': ' + String(value)).join(' · ')
    : typeof error.body.field === 'string' ? error.body.field : '';
  return t('ورودی نامعتبر است.', 'Invalid input.') + (detail ? ' ' + detail : '');
}
