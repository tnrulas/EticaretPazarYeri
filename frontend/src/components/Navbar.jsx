import React, { useEffect } from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import '../style/Navbar.css'
import { useState } from 'react';
import api from '../services/api';
import '../style/filters.css'


function Navbar() {
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');
    const [burgerOpen, setBurgerOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [user, setUser] = useState(null)
    const [categorys, setCategorys] = useState([])
    const [categoryOpen, setCategoryOpen] = useState(false);
    const [subCategoryOpen, setSubCategoryOpen] = useState(false);
    const [subOpen, setSubOpen] = useState(null)

    const isSeller = localStorage.getItem('is_seller') === 'true';

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await api.get('urunler/kategoriler/')
                console.log(response.data)
                setCategorys(response.data)
            } catch (error) {
                console.error("kategorileri çekerken bir hata oluştu", error)
            }
        }
        fetchCategories();
    }, [])

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('accounts/listele/')
                console.log('KATEGORİLER:', response.data)
                setUser(response.data)
            } catch (error) {
                console.error("KUllanıcı çekilirken bir hata oluştu:", error)
            }
        }
        fetchUser();
    }, [])

    const handleCategory = (category) => {
        setSelectedCategory(category);
        setBurgerOpen(false);
        navigate(`/filter?category=${category.id}&name=${encodeURIComponent(category.name)}`);
    }

    const handleSearch = (e) => {
        if (e.key == 'Enter' && searchTerm.trim() !== '') {
            navigate(`/search?q=${searchTerm}`)
        }
    }

    return (
        <nav className='navbar-wrapper'>
            <div className="navbar-left">
                <button
                    className="burger-btn"
                    type="button"
                    onClick={() => setBurgerOpen(true)}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z" /></svg>
                </button>
                <h2 className="navbar-logo" onClick={() => navigate('/')}>
                    E-Pazar
                </h2>
            </div>

            <div
                className={`offcanvas offcanvas-start custom-sidebar ${burgerOpen ? 'show' : ''}`}
                tabIndex="-1"
            >
                <div className="offcanvas-header sidebar-header">
                    <h5 className="sidebar-title">Kategoriler</h5>
                    <button
                        type="button"
                        className="btn-close"
                        onClick={() => setBurgerOpen(false)}
                        aria-label="Close"
                    ></button>
                </div>
                <div className="offcanvas-body sidebar-body">
                    <div
                        className="sidebar-item sidebar-item-favorite"
                        onClick={() => {
                            navigate('/favoriler');
                            setBurgerOpen(false);
                        }}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" /></svg>
                        Favorilerim
                    </div>

                    <ul className="sidebar-menu">
                        {categorys.map((category) => (
                            <li key={category.id} className="sidebar-item">
                                <div onClick={() => setCategoryOpen(categoryOpen === category.id ? null : category.id)}>
                                    {category.name}
                                </div>

                                {categoryOpen === category.id && (
                                    <ul>
                                        {category.subcategories.map((sub) => (
                                            <li
                                                key={sub.id}
                                                onMouseEnter={() => setSubOpen(sub.id)}
                                                onMouseLeave={() => setSubOpen(null)}
                                            >
                                                <div onClick={() => handleCategory(sub)}>
                                                    {sub.name}
                                                </div>

                                                {subOpen === sub.id && sub.subcategories.length > 0 && (
                                                    <ul>
                                                        {sub.subcategories.map((alt) => (
                                                            <li key={alt.id} onClick={() => handleCategory(alt)}>
                                                                {alt.name}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                )}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </li>
                        ))}
                    </ul>

                </div>
            </div>


            {burgerOpen && (
                <div
                    className="offcanvas-backdrop fade show"
                    onClick={() => setBurgerOpen(false)}
                ></div>
            )}

            <div className="navbar-center">
                <div className="search-container">
                    <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    <input
                        className="search-input"
                        type='text'
                        placeholder='Ürün, kategori veya marka ara...'
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onKeyDown={handleSearch}>
                    </input>
                </div>
            </div>

            <div className="navbar-right">
                <div className="nav-links">
                    <span className='nav-link' onClick={() => navigate('/siparislerim')}>Siparişlerim</span>
                    <span className="nav-link" onClick={() => navigate('/sepet')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                        Sepetim
                    </span>
                    {isSeller && (
                        <>
                            <span
                                className="nav-link"
                                onClick={() => user?.id && navigate(`/saticiMesajlar/${user.id}`)}
                                style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                </svg>
                                Mesajlar
                            </span>

                            <span
                                className="nav-link seller-badge"
                                onClick={() => navigate('/urunOlustur')}
                            >
                                + Ürün Ekle
                            </span>
                        </>
                    )}
                </div>

                {user === null ? (
                    <div className="user-profile-badge" onClick={() => navigate('/giris')}>
                        <div className="user-avatar" style={{ background: '#E2E8F0', color: '#475569' }}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" /></svg>
                        </div>
                        <div className="user-info">
                            <span className="user-name">Giriş Yap</span>
                            <span className="user-role">Kayıt Ol</span>
                        </div>
                    </div>
                ) : (
                    <div className="user-profile-badge" onClick={() => navigate('/dashboard')}>
                        <div className="user-avatar">
                            {user.username.charAt(0).toUpperCase()}
                        </div>
                        <div className="user-info">
                            <span className="user-name">{user.username}</span>
                            <span className="user-role">
                                {isSeller ? 'Satıcı' : 'Müşteri'}
                            </span>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    )
}

export default Navbar;