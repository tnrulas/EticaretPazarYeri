import React from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import '../style/Navbar.css'

function Navbar() {
    const navigate = useNavigate();

    const isSeller = localStorage.getItem('is_seller') === 'true';

    return (
        <nav className='navbar'>
            <h2 className="navbar__logo" onClick={() => navigate('/')} >
                Benim E-ticaret Sitem
            </h2>
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