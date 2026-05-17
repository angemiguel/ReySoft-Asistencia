import { createContext, ReactNode, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { api } from '../api/client';
import { User } from '../types';

interface LoginResponse {
  access_token: string;
  user: User;
}

interface AuthContextValue {
  token: string | null;
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function applyOrganizationTheme(user: User | null) {
  const organization = user?.organization;
  document.documentElement.style.setProperty('--primary-color', organization?.primary_color ?? '#2563EB');
  document.documentElement.style.setProperty('--secondary-color', organization?.secondary_color ?? '#1E293B');
  document.documentElement.style.setProperty('--accent-color', organization?.accent_color ?? '#F59E0B');
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('reysoft_asistencia_token'));
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(Boolean(token));
  const mountedRef = useRef(true);

  useEffect(() => {
    return () => { mountedRef.current = false; };
  }, []);

  const refreshUser = useCallback(async () => {
    if (!localStorage.getItem('reysoft_asistencia_token')) {
      setLoading(false);
      return;
    }
    try {
      const response = await api.get<User>('/auth/me');
      if (mountedRef.current) {
        setUser(response.data);
        applyOrganizationTheme(response.data);
      }
    } catch {
      localStorage.removeItem('reysoft_asistencia_token');
      if (mountedRef.current) {
        setToken(null);
        setUser(null);
        applyOrganizationTheme(null);
      }
    } finally {
      if (mountedRef.current) setLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await api.post<LoginResponse>('/auth/login', { email, password });
    localStorage.setItem('reysoft_asistencia_token', response.data.access_token);
    setToken(response.data.access_token);
    setUser(response.data.user);
    applyOrganizationTheme(response.data.user);
    return response.data.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('reysoft_asistencia_token');
    setToken(null);
    setUser(null);
    applyOrganizationTheme(null);
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const value = useMemo(
    () => ({ token, user, loading, login, logout, refreshUser }),
    [token, user, loading, login, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return value;
}

