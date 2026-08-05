import React from 'react'
import { Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../services/constants'
import api from "../services/api"
import { jwtDecode } from "jwt-decode"


function ProtectedRoute({ children }) {

    const [isAuthenticated, setIsAuthorized] = useState(null);

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false))
    }, [])

    const refresh = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);

        if (!refreshToken) {
            setIsAuthorized(false);
            return
        }

        try {
            const response = await api.post("accounts/auth/yenile/", {
                refresh: refreshToken
            });
            if (response.status === 200) {
                const newAccess = response.data.access;
                localStorage.setItem(ACCESS_TOKEN, newAccess);

                setIsAuthorized(true);
            }
        } catch (error) {
            setIsAuthorized(false);
        }
    }


    const auth = async () => {
        const accessToken = localStorage.getItem(ACCESS_TOKEN)

        if (!accessToken) {
            setIsAuthorized(false);
            return
        }

        try {
            const decoded = jwtDecode(accessToken)
            const now = Date.now() / 1000

            if (decoded.exp < now) {
                await refresh()
            } else {
                setIsAuthorized(true)
            }
        } catch (err) {
            setIsAuthorized(false);
        }
    }

    if (isAuthenticated === null) {
        return <div>Loading...</div>
    }

    return isAuthenticated ? children : <Navigate to="/giris" />
}

export default ProtectedRoute