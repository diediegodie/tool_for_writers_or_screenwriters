import { describe, it, beforeEach, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Register from '../Register';
import axios from 'axios';

vi.mock('axios');
const mockedAxios = axios as any;

describe('Register Page', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders register form', () => {
    render(<Register />);
    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
  });

  it('validates empty fields', async () => {
    render(<Register />);
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    expect(screen.getByPlaceholderText(/email/i)).toHaveAttribute('required');
    expect(screen.getByPlaceholderText(/password/i)).toHaveAttribute('required');
  });

  it('handles successful registration', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { token: 'jwt-token' } });
    render(<Register />);
    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    await waitFor(() => expect(localStorage.getItem('token')).toBe('jwt-token'));
  });

  it('handles registration failure', async () => {
    mockedAxios.post.mockRejectedValueOnce({ response: { data: { message: 'Registration failed' } } });
    render(<Register />);
    fireEvent.change(screen.getByPlaceholderText(/email/i), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => expect(screen.getByText(/registration failed/i)).toBeInTheDocument());
  });
});

