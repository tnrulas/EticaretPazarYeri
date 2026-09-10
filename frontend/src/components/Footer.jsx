import React from "react";
import '../style/Footer.css'

function Footers() {
    return (
        <footer className="footer">
            <div className="footer__container">

                <div className="footer__column">
                    <h3 className="footer__title">Hakkımızda</h3>
                    <p className="footer__text">
                        En yeni ürünleri en uygun fiyatlarla kapınıza getiriyoruz. Güvenli alışverişin ve hızlı teslimatın adresi.
                    </p>
                </div>

                <div className="footer__column">
                    <h3 className="footer__title">Müşteri Hizmetleri</h3>
                    <ul className="footer__list">
                        <li><a href="#" className="footer__link">Sıkça Sorulan Sorular</a></li>
                        <li><a href="#" className="footer__link">İade ve Değişim</a></li>
                        <li><a href="#" className="footer__link">Kargo Takip</a></li>
                        <li><a href="#" className="footer__link">İletişim</a></li>
                    </ul>
                </div>

                <div className="footer__column">
                    <h3 className="footer__title">Bizi Takip Edin</h3>
                    <ul className="footer__list">
                        <li><a href="#" className="footer__link">📸 Instagram</a></li>
                        <li><a href="#" className="footer__link">🐦 Twitter (X)</a></li>
                        <li><a href="#" className="footer__link">💼 LinkedIn</a></li>
                    </ul>
                </div>

            </div>

            <div className="footer__bottom">
                &copy; {new Date().getFullYear()} E-Ticaret Projesi. Tüm Hakları Saklıdır.
            </div>
        </footer>
    )
}

export default Footers