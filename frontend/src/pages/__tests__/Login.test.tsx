
import { describe, it, beforeEach, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from '../Login';
import axios from 'axios';

vi.mock('axios');
const mockedAxios = axios as any;

describe('Login Page', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders login form', () => {
    render(<Login />);
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('validates empty fields', async () => {
    render(<Login />);
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    expect(screen.getByPlaceholderText(/email/i)).toHaveAttribute('required');
    expect(screen.getByPlaceholderText(/password/i)).toHaveAttribute('required');
  });

  it('handles successful login', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { token: 'jwt-token' } });
    render(<Login />);
    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    await waitFor(() => expect(localStorage.getItem('token')).toBe('jwt-token'));
  });

  it('handles login failure', async () => {
    mockedAxios.post.mockRejectedValueOnce({ response: { data: { message: 'Login failed' } } });
    render(<Login />);
    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    await waitFor(() => expect(screen.getByText(/login failed/i)).toBeTruthy());
  });
});
