import { cloneElement, useId, useState } from 'react';
import type { FormEvent, ReactElement } from 'react';
import { errorText } from './api';
import type { Translate } from './api';

export function useTask(t: Translate) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function run(task: () => Promise<void>) {
    if (busy) return;
    setBusy(true);
    setError('');
    try { await task(); }
    catch (cause) { setError(errorText(cause, t)); }
    finally { setBusy(false); }
  }
  return { busy, error, run };
}

export function Field({ label, children }: { label: string; children: ReactElement<{ id?: string }> }) {
  const id = useId();
  return <div className="field"><label htmlFor={id}>{label}</label>{cloneElement(children, { id })}</div>;
}

export function Message({ text, error = false }: { text: string; error?: boolean }) {
  return text ? <p className={'message' + (error ? ' error' : '')} role={error ? 'alert' : 'status'}>{text}</p> : null;
}

export function formValues(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  return Object.fromEntries(new FormData(event.currentTarget)) as Record<string, string>;
}
