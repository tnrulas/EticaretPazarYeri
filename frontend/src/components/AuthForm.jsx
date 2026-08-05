import React from 'react'
import { useEffect, useState } from 'react'
import api from '../services/api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../services/constants'
import { useNavigate } from "react-router-dom"


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
                url = 'auth/giris/'
                payload = { username, password }
            } else if (method === 'kayit' && kayitTipi === 'bireysel') {
                url = 'auth/kayit/musteri'
                payload = { username, email, password }
            } else if (method === 'kayit' && kayitTipi === 'kurumsal') {
                url = 'auth/kayit/satici'
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

                navigate("/Anasayfa")
            } else {
                navigate('/Giris')
            }

        } catch (error) {
            console.error(error);
            alert("İşlem başarısız oldu. Lütfen bilgilerinizi kontrol edin.");
        }
    }

    return (
        <div className='girisregisterform'>
            <h2>{method === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}</h2>

            {method === 'kayit' && (
                <div>
                    <div>
                        <input
                            type='radio'
                            id="bireysel"
                            value='bireysel'
                            checked={kayitTipi === 'bireysel'}
                            onChange={(e) => setKayitTipi(e.target.value)} />
                        <label htmlFor="bireysel">Bireysel Kayıt</label>
                    </div>
                    <div>
                        <input
                            type='radio'
                            id="kurumsal"
                            value='kurumsal'
                            checked={kayitTipi === 'kurumsal'}
                            onChange={(e) => setKayitTipi(e.target.value)} />
                        <label htmlFor="kurumsal">Kurumsal Üyelik</label>
                    </div>
                </div>
            )}
            <form onSubmit={handleSubmit}>
                {method === 'login' && (
                    <>
                        <input type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                        <input type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </>
                )}

                {method === 'kayit' && kayitTipi === 'bireysel' && (
                    <>
                        <input type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                        <input type="email" placeholder="E-posta" value={email} onChange={(e) => setEmail(e.target.value)} required />
                        <input type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </>
                )}

                {method === 'kayit' && kayitTipi == 'kurumsal' && (
                    <>
                        <input type="text" placeholder="Firma Adı" value={companyName} onChange={(e) => setCompanyName(e.target.value)} required />
                        <input type="text" placeholder="Kullanıcı Adı" value={username} onChange={(e) => setUsername(e.target.value)} required />
                        <input type="email" placeholder="E-posta" value={email} onChange={(e) => setEmail(e.target.value)} required />
                        <input type="text" placeholder="Firma Adresi" value={companyAddress} onChange={(e) => setCompanyAddress(e.target.value)} required />
                        <input type="number" placeholder="Firma Telefonu" value={companyPhone} onChange={(e) => setCompanyPhone(e.target.value)} required />
                        <input type="password" placeholder="Şifre" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </>
                )}

                <button type="submit" style={{ marginTop: '15px' }}>
                    {method === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}
                </button>
            </form>

        </div>
    )
}

export default Form