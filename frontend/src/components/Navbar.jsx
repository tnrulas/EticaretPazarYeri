import React, { useEffect } from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import '../style/Navbar.css'
import { useState } from 'react';
import api from '../services/api';


function Navbar() {
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');
    const [burgerOpen, setBurgerOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [user, setUser] = useState(null)

    const isSeller = localStorage.getItem('is_seller') === 'true';

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('accounts/listele/')
                setUser(response.data)
            } catch (error) {
                console.error("KUllanıcı çekilirken bir hata oluştu:", error)
            }
        }
        fetchUser();
    }, [])

    const handleCategory = (category_name) => {
        setSelectedCategory(category_name);
        setBurgerOpen(false);
        navigate(`/filter?category=${encodeURIComponent(category_name)}`);
    }

    const handleSearch = (e) => {
        if (e.key == 'Enter' && searchTerm.trim() !== '') {
            navigate(`/search?q=${searchTerm}`)
        }
    }

    return (
        <nav className='navbar'>
            <button
                className="btn"
                type="button"
                onClick={() => setBurgerOpen(true)}
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 6h-24v-4h24v4zm0 4h-24v4h24v-4zm0 8h-24v4h24v-4z" /></svg>
            </button>

            <div
                className={`offcanvas offcanvas-start ${burgerOpen ? 'show' : ''}`}
                style={{ visibility: burgerOpen ? 'visible' : 'hidden' }}
                tabIndex="-1"
            >
                <div className="offcanvas-header">
                    <h5 className="offcanvas-title">Kategoriler</h5>

                    <button
                        type="button"
                        className="btn-close"
                        onClick={() => setBurgerOpen(false)}
                        aria-label="Close"
                    ></button>
                </div>
                <div className="offcanvas-body">

                    <ul className="list-group list-group-flush">
                        <li onClick={() => handleCategory('Elektronik')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Elektronik</li>
                        <li onClick={() => handleCategory('Moda & Giyim')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Moda & Giyim</li>
                        <li onClick={() => handleCategory('Ev, Mobilya & Yaşam')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Ev, Mobilya & Yaşam</li>
                        <li onClick={() => handleCategory('Kozmetik & Kişisel Bakım')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Kozmetik & Kişisel Bakım</li>
                        <li onClick={() => handleCategory('Anne, Bebek & Oyuncak')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Anne, Bebek & Oyuncak</li>
                        <li onClick={() => handleCategory('Spor & Outdoor')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Spor & Outdoor</li>
                        <li onClick={() => handleCategory('Süpermarket & Gıda')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Süpermarket & Gıda</li>
                        <li onClick={() => handleCategory('Kitap, Müzik & Hobi')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Kitap, Müzik & Hobi</li>
                        <li onClick={() => handleCategory('Otomobil & Motosiklet')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Otomobil & Motosiklet</li>
                        <li onClick={() => handleCategory('Evcil Hayvan Ürünleri')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Evcil Hayvan Ürünleri</li>
                        <li onClick={() => handleCategory('Ofis & Kırtasiye')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Ofis & Kırtasiye</li>
                        <li onClick={() => handleCategory('Saat, Takı & Aksesuar')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Saat, Takı & Aksesuar</li>
                        <li onClick={() => handleCategory('Ayakkabı & Çanta')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Ayakkabı & Çanta</li>
                        <li onClick={() => handleCategory('Yapı Market & Hırdavat')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Yapı Market & Hırdavat</li>
                        <li onClick={() => handleCategory('Bahçe & Teras')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Bahçe & Teras</li>
                        <li onClick={() => handleCategory('Oyun & Konsol')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Oyun & Konsol</li>
                        <li onClick={() => handleCategory('Sağlık & Medikal Ürünler')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Sağlık & Medikal Ürünler</li>
                        <li onClick={() => handleCategory('Müzik Aletleri')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Müzik Aletleri</li>
                        <li onClick={() => handleCategory('Sanat, Hobi & El İşi')} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }} className="list-group-item list-group-item-action" style={{ cursor: 'pointer' }}>Sanat, Hobi & El İşi</li>
                    </ul>
                </div>
            </div>


            {burgerOpen && (
                <div
                    className="offcanvas-backdrop fade show"
                    onClick={() => setBurgerOpen(false)}
                ></div>
            )}


            <h2 className="navbar__logo" onClick={() => navigate('/')} >
                Benim E-ticaret Sitem
            </h2>


            <input
                type='text'
                placeholder='ara'
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={handleSearch}>
            </input>

            {user === null ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }} onClick={() => navigate('/giris')}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#ccc', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        👤
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ fontSize: '14px', fontWeight: 'bold' }}>Giriş Yap</span>
                        <span style={{ fontSize: '12px', color: 'gray' }}>Hesap Yok</span>
                    </div>
                </div>
            ) : (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }} onClick={() => navigate('/dashboard')}>
                    <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#007bff', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '18px' }}>
                        {user.username.charAt(0).toUpperCase()}
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ fontSize: '14px', fontWeight: 'bold' }}>{user.username}</span>
                        <span style={{ fontSize: '12px', color: 'gray' }}>
                            {isSeller ? 'Satıcı Hesabı' : 'Müşteri Hesabı'}
                        </span>
                    </div>
                </div>
            )}

            <div className="navbar__links">
                <span className='navbar__link' onClick={() => navigate('/siparislerim')}>Siparişlerim</span>
                <span className="navbar__link" onClick={() => navigate('/sepet')}>Sepetim</span>
                {isSeller && (
                    <span
                        className="navbar__link navbar__link--seller"
                        onClick={() => navigate('/urunOlustur')}
                    >
                        Ürün Ekle
                    </span>
                )}
            </div>
        </nav>
    )
}

export default Navbar;