import React from "react";


function Footers() {
    return (
        <footer style={{ backgroundColor: '#232f3e', color: 'white', padding: '40px 20px', marginTop: 'auto' }}>
            <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>

                <div style={{ flex: '1', minWidth: '200px' }}>
                    <h3 style={{ borderBottom: '2px solid #ff9900', paddingBottom: '10px', display: 'inline-block' }}>Hakkımızda</h3>
                    <p style={{ fontSize: '14px', lineHeight: '1.6', marginTop: '10px', color: '#ccc' }}>
                        En yeni ürünleri en uygun fiyatlarla kapınıza getiriyoruz. Güvenli alışverişin ve hızlı teslimatın adresi.
                    </p>
                </div>

                <div style={{ flex: '1', minWidth: '200px' }}>
                    <h3 style={{ borderBottom: '2px solid #ff9900', paddingBottom: '10px', display: 'inline-block' }}>Müşteri Hizmetleri</h3>
                    <ul style={{ listStyle: 'none', padding: 0, marginTop: '10px', lineHeight: '2' }}>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>Sıkça Sorulan Sorular</a></li>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>İade ve Değişim</a></li>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>Kargo Takip</a></li>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>İletişim</a></li>
                    </ul>
                </div>

                <div style={{ flex: '1', minWidth: '200px' }}>
                    <h3 style={{ borderBottom: '2px solid #ff9900', paddingBottom: '10px', display: 'inline-block' }}>Bizi Takip Edin</h3>
                    <ul style={{ listStyle: 'none', padding: 0, marginTop: '10px', lineHeight: '2' }}>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>📸 Instagram</a></li>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>🐦 Twitter (X)</a></li>
                        <li><a href="#" style={{ color: '#ccc', textDecoration: 'none' }}>💼 LinkedIn</a></li>
                    </ul>
                </div>

            </div>

            <div style={{ textAlign: 'center', borderTop: '1px solid #444', marginTop: '30px', paddingTop: '20px', fontSize: '14px', color: '#888' }}>
                &copy; {new Date().getFullYear()} E-Ticaret Projesi. Tüm Hakları Saklıdır.
            </div>
        </footer>
    )
}

export default Footers