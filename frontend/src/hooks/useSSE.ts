import { useEffect, useRef, useCallback } from 'react';
import { SSEEvent } from '../types';

const getApiUrl = (): string => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:3011`;
  }
  return 'http://localhost:3011';
};

type SSEHandler = (event: string, data: any) => void;

export function useSSE(onEvent: SSEHandler) {
  const handlerRef = useRef(onEvent);
  handlerRef.current = onEvent;
  const esRef = useRef<EventSource | null>(null);

  const connect = useCallback(() => {
    if (esRef.current) esRef.current.close();
    
    const apiUrl = getApiUrl();
    const es = new EventSource(`${apiUrl}/api/events`);
    esRef.current = es;

    const handle = (type: string) => (e: MessageEvent) => {
      try {
        handlerRef.current(type, JSON.parse(e.data));
      } catch (error) {
        console.warn('Failed to parse SSE data:', error);
      }
    };

    es.addEventListener('init', handle('init'));
    es.addEventListener('job_update', handle('job_update'));
    es.addEventListener('job_created', handle('job_created'));
    es.addEventListener('job_deleted', handle('job_deleted'));
    es.addEventListener('jobs_cleared', handle('jobs_cleared'));

    es.onopen = () => {
      console.log('SSE connection opened');
    };

    es.onerror = (error) => {
      console.warn('SSE connection error, reconnecting in 3 seconds...', error);
      es.close();
      setTimeout(connect, 3000);
    };
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (esRef.current) {
        esRef.current.close();
      }
    };
  }, [connect]);

  const disconnect = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }
  }, []);

  return { disconnect };
}