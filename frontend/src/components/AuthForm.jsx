import React from 'react'
import { useEffect, useState } from 'react'
import api from '../services/api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../services/constants'
import { useNavigate } from "react-router-dom"
import '../style/Form.css'


function Form({ method }) {

    const [kayitTipi, setKayitTipi] = useState("bireysel")
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [companyName, setCompanyName] = useState('')
    const [companyAddress, setCompanyAddress] = useState('')
    const [companyPhone, setCompanyPhone] = useState('')

    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        localStorage.removeItem(ACCESS_TOKEN)
        localStorage.removeItem(REFRESH_TOKEN)

        try {
            let url = ''
            let payload = {};

            if (method === 'login') {
                url = 'accounts/auth/giris/'
                payload = { username, password }
            } else if (method === 'kayit' && kayitTipi === 'bireysel') {
                url = 'accounts/auth/kayit/musteri'
                payload = { username, email, password }
            } else if (method === 'kayit' && kayitTipi === 'kurumsal') {
                url = 'accounts/auth/kayit/satici'
                payload = {
                    username,
                    email,
                    company_name: companyName,
                    company_address: companyAddress,
                    company_phone: companyPhone,
                    password
                };
            } else {
                alert('geçersiz işlem');
                return;
            }

            const res = await api.post(url, payload);

            if (method === 'login') {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
                localStorage.setItem('is_seller', res.data.is_seller);
                localStorage.setItem('username', res.data.username);
                window.location.href = "/";

                navigate("/")
            } else {
                navigate('/giris')
            }

        } catch (error) {
            console.error(error);
            alert("İşlem başarısız oldu. Lütfen bilgilerinizi kontrol edin.");
        }
    }

    return (
        <div className="auth">
            <div className="auth__card">
                <p className="auth__eyebrow">
                    {method === 'login' ? 'Tekrar hoş geldiniz' : 'Aramıza katılın'}
                </p>
                <h2 className="auth__title">{method === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}</h2>

                {method === 'kayit' && (
                    <div className="auth__toggle" role="radiogroup" aria-label="Kayıt tipi">
                        <label className={`auth__toggle-option ${kayitTipi === 'bireysel' ? 'is-active' : ''}`}>
                            <input
                                type='radio'
                                id="bireysel"
                                value='bireysel'
                                checked={kayitTipi === 'bireysel'}
                                onChange={(e) => setKayitTipi(e.target.value)} />
                            Bireysel Kayıt
                        </label>
                        <label className={`auth__toggle-option ${kayitTipi === 'kurumsal' ? 'is-active' : ''}`}>
                            <input
                                type='radio'
                                id="kurumsal"
                                value='kurumsal'
                                checked={kayitTipi === 'kurumsal'}
                                onChange={(e) => setKayitTipi(e.target.value)} />
                            Kurumsal Üyelik
                        </label>
                    </div>
                )}
                <form className="auth__form" onSubmit={handleSubmit}>
                    {method === 'login' && (
                        <>
                            <input className="auth__input" type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                            <input className="auth__input" type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                        </>
                    )}

                    {method === 'kayit' && kayitTipi === 'bireysel' && (
                        <>
                            <input className="auth__input" type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                            <input className="auth__input" type="email" placeholder="E-posta" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            <input className="auth__input" type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                        </>
                    )}

                    {method === 'kayit' && kayitTipi == 'kurumsal' && (
                        <>
                            <input className="auth__input" type="text" placeholder="Firma Adı" value={companyName} onChange={(e) => setCompanyName(e.target.value)} required />
                            <input className="auth__input" type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                            <input className="auth__input" type="email" placeholder="E-posta" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            <input className="auth__input" type="text" placeholder="Firma Adresi" value={companyAddress} onChange={(e) => setCompanyAddress(e.target.value)} required />
                            <input className="auth__input" type="number" placeholder="Firma Telefonu" value={companyPhone} onChange={(e) => setCompanyPhone(e.target.value)} required />
                            <input className="auth__input" type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                        </>
                    )}

                    <button type="submit" className="auth__submit">
                        {method === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}
                    </button>
                </form>
            </div>
        </div>
    )
}

export default Form