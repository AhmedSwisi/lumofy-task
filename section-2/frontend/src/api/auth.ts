import api from "./router";
import { useMutation } from "react-query";
import Cookies from 'js-cookie';
import { AxiosError } from "axios";

interface AuthResponse {
    access:string;
    refresh:string
}

interface LoginInput {
  username: string;
  password: string;
}

export const loginRequest = async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/token/', { username, password });
    const { access, refresh } = response.data;
  
    // Save tokens in cookies
    Cookies.set('accessToken', access, { expires: 1 }); // Token expires in 1 day
    Cookies.set('refreshToken', refresh, { expires: 7 }); // Refresh token expires in 7 days
  
    return response.data;
  };
  
  // Logout function: Remove tokens from cookies
  export const logout = (): void => {
    Cookies.remove('accessToken');
    Cookies.remove('refreshToken');
  };
  
  // Get the access token from cookies
  export const getToken = (): string | undefined => {
    return Cookies.get('accessToken');
  };
  
  // Get the refresh token from cookies
  export const getRefreshToken = (): string | undefined => {
    return Cookies.get('refreshToken');
  };
  
  // Refresh the token using the refresh token from cookies
  export const refreshToken = async (): Promise<string | null> => {
    const refreshToken = getRefreshToken();
    
    if (refreshToken) {
      try {
        const response = await api.post<AuthResponse>('/token/refresh/', {
          refresh: refreshToken,
        });
  
        // Update the access token in cookies
        Cookies.set('accessToken', response.data.access, { expires: 1 });
  
        return response.data.access;
      } catch (error) {
        throw new Error('Token refresh failed: ' + error);
      }
    }
  
    return null;
  };

  export const useLogin = () => {
    return useMutation(
      ({ username, password }: LoginInput) => loginRequest(username, password),
      {
        onSuccess: (data) => {
          // Optionally handle success, like redirecting the user or showing a success message
          console.log('Login successful:', data);
          window.location.href = '/protected'; // Example of redirecting after login
        },
        onError: (error: AxiosError) => {
          // Optionally handle error, such as displaying a notification
          console.error('Login failed:', error);
        },
      }
    );
  };