import React from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import '../style/Navbar.css'
import { useState } from 'react';

function Navbar() {
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');

    const isSeller = localStorage.getItem('is_seller') === 'true';

    const handleSearch = (e) => {
        if (e.key == 'Enter' && searchTerm.trim() !== '') {
            navigate(`/search?q=${searchTerm}`)
        }
    }

    return (
        <nav className='navbar'>
            <h2 className="navbar__logo" onClick={() => navigate('/')} >
                Benim E-ticaret Sitem
            </h2>
            <input
                type='text'
                placeholder='ara'
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={handleSearch}>
            </input>
            <div className="navbar__links">
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