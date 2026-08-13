import React from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import '../style/Sepetlistesi.css'

function SepetListesi() {
    const navigate = useNavigate();

    const cartItems = useSelector((state) => state.cart.cartItems) || [];

    const toplamFiyat = cartItems.reduce((acc, urun) => {
        const adet = urun.quantity || 1;
        return acc + (parseFloat(urun.price) * adet);
    }, 0);

    return (
        <div className="cart">
            <div className="cart__header">
                <p className="cart__eyebrow">Sepetiniz</p>
                <h1 className="cart__title">{cartItems.length} ürün</h1>
            </div>

            {cartItems.length === 0 ? (
                <p className="cart__empty">Sepetiniz boş. Ürünler sayfasından alışverişe başlayabilirsiniz.</p>
            ) : (
                <ul className="cart__list">
                    {cartItems.map((ürün, index) => (
                        <li key={ürün.id || index} className="cart-item">
                            <div className="cart-item__info">
                                <span className="cart-item__name">{ürün.name}</span>
                                <span className="cart-item__qty">Adet: {ürün.quantity}</span>
                            </div>
                            <span className="cart-item__price">{ürün.price} ₺</span>
                        </li>
                    ))}
                </ul>
            )}

            <div className="cart__summary">
                <span className="cart__summary-label">Toplam Fiyat</span>
                <span className="cart__summary-total">{toplamFiyat} ₺</span>
            </div>

            <button
                className="cart__checkout"
                onClick={() => navigate('/odeme')}
                disabled={cartItems.length === 0}
            >
                Ödeme Ekranına Git
            </button>
        </div>
    )
}

export default SepetListesi