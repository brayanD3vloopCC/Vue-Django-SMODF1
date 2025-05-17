import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const userService = {
    async getCurrentUser() {
        try {
            const response = await axios.get(`${API_URL}/users/me/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching user data:', error);
            throw error;
        }
    },

    async updateUserProfile(userData) {
        try {
            const response = await axios.put(`${API_URL}/users/me/`, userData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error updating user profile:', error);
            throw error;
        }
    }
}; 