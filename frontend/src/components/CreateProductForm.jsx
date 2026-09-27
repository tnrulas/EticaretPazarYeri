import React from 'react'
import { useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../style/Urunolustur.css'

function UrunOlustur() {
    const navigate = useNavigate();

    const [urunIsmi, setUrunIsmi] = useState('');
    const [urunAciklamasi, setUrunAciklamasi] = useState('');
    const [urunResmi, setUrunResmi] = useState(null);
    const [urunFiyati, setUrunFiyati] = useState('');
    const [stokSayisi, setStokSayisi] = useState('');
    const [ekstraResim, setEkstraResim] = useState([]);

    const [kategoriler, setKategoriler] = useState([]);

    const [seciliAnaKategori, setSeciliAnaKategori] = useState('');
    const [seciliAltKategori, setSeciliAltKategori] = useState('');
    const [seciliEnAltKategori, setSeciliEnAltKategori] = useState('');

    const [isBulkSale, setIsBulkSale] = useState(false);
    const [isGiftWrap, setIsGiftWrap] = useState(false);
    const [hasVideo, setHasVideo] = useState(false);
    const [isCampaign, setIsCampaign] = useState(false);
    const [isBuyTogether, setIsBuyTogether] = useState(false);
    const [isBuyMorePayLess, setIsBuyMorePayLess] = useState(false);
    const [isCorporateInvoice, setIsCorporateInvoice] = useState(false);
    const [isEditorChoice, setIsEditorChoice] = useState(false);

    const [dinamikDegerler, setDinamikDegerler] = useState({});

    useEffect(() => {
        const kategorileriGetir = async () => {
            try {
                const res = await api.get('urunler/kategoriler/');
                setKategoriler(res.data);
            } catch (error) {
                console.error("Kategoriler çekilirken hata:", error);
            }
        };
        kategorileriGetir();
    }, []);

    const olustur = async (e) => {
        e.preventDefault();

        const nihaiKategoriId = seciliEnAltKategori || seciliAltKategori || seciliAnaKategori;

        if (!nihaiKategoriId) {
            alert("Lütfen en az bir kategori seçin.");
            return;
        }

        try {
            const isSeller = localStorage.getItem('is_seller');
            if (isSeller !== 'true') {
                alert('Ürün oluşturmak için satıcı olmanız gerekmektedir.');
                return;
            }
            const formData = new FormData();
            formData.append('name', urunIsmi);
            formData.append('description', urunAciklamasi);
            formData.append('price', urunFiyati);
            formData.append('stock_count', stokSayisi);
            formData.append('category', nihaiKategoriId);

            formData.append('is_bulk_sale', isBulkSale);
            formData.append('is_gift_wrap', isGiftWrap);
            formData.append('has_video', hasVideo);
            formData.append('is_campaign', isCampaign);
            formData.append('is_buy_together', isBuyTogether);
            formData.append('is_buy_more_pay_less', isBuyMorePayLess);
            formData.append('is_corporate_invoice', isCorporateInvoice);
            formData.append('is_editor_choice', isEditorChoice);

            formData.append('dinamik_ozellikler', JSON.stringify(dinamikDegerler));

            if (urunResmi) {
                formData.append('photo', urunResmi);
            }

            if (ekstraResim.length > 0) {
                for (let resim of ekstraResim) {
                    formData.append('images', resim);
                }
            }

            const res = await api.post('urunler/Urunekle/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('Ürün başarı ile oluşturuldu!');
            navigate("/");

        } catch (error) {
            if (error.response && error.response.data) {
                console.error("Django'nun reddetme sebebi:", error.response.data);
                alert(`Kayıt Başarısız!\nSebep: ${JSON.stringify(error.response.data)}`);
            } else {
                console.error("Ürün oluşturulurken hata oluştu.", error);
                alert("İşlem başarısız oldu. Sunucuya ulaşılamıyor.");
            }
        }
    }

    const aktifAltKategoriler = kategoriler.find(k => k.id === parseInt(seciliAnaKategori))?.subcategories || [];
    const aktifEnAltKategoriler = aktifAltKategoriler.find(k => k.id === parseInt(seciliAltKategori))?.subcategories || [];


    let toplananOzellikler = [];

    const anaCat = kategoriler.find(k => k.id === parseInt(seciliAnaKategori));
    if (anaCat && anaCat.ozellikler) {
        toplananOzellikler = [...toplananOzellikler, ...anaCat.ozellikler];
    }

    const altCat = aktifAltKategoriler.find(k => k.id === parseInt(seciliAltKategori));
    if (altCat && altCat.ozellikler) {
        toplananOzellikler = [...toplananOzellikler, ...altCat.ozellikler];
    }

    const enAltCat = aktifEnAltKategoriler.find(k => k.id === parseInt(seciliEnAltKategori));
    if (enAltCat && enAltCat.ozellikler) {
        toplananOzellikler = [...toplananOzellikler, ...enAltCat.ozellikler];
    }

    return (
        <div className="product-form">
            <div className="product-form__card">
                <p className="product-form__eyebrow">Satıcı paneli</p>
                <h1 className="product-form__title">Ürün Oluştur</h1>
                <form className="product-form__form" onSubmit={olustur}>

                    <div className="product-form__field">
                        <label>Ürün İsmi</label>
                        <input type="text" value={urunIsmi} onChange={(e) => setUrunIsmi(e.target.value)} required />
                    </div>

                    <div className="product-form__field">
                        <label>Açıklama</label>
                        <textarea value={urunAciklamasi} onChange={(e) => setUrunAciklamasi(e.target.value)} required />
                    </div>

                    <div className="product-form__row">
                        <div className="product-form__field">
                            <label>Fiyat (₺)</label>
                            <input type="number" value={urunFiyati} onChange={(e) => setUrunFiyati(e.target.value)} required />
                        </div>
                        <div className="product-form__field">
                            <label>Stok Sayısı</label>
                            <input type="number" value={stokSayisi} onChange={(e) => setStokSayisi(e.target.value)} required />
                        </div>
                    </div>

                    <div className="product-form__field product-form__field--file">
                        <label>Ürün Kapak Resmi</label>
                        <input type="file" accept="image/*" onChange={(e) => setUrunResmi(e.target.files[0])} />
                    </div>

                    <div className="product-form__field product-form__field--file">
                        <label>Ürün diğer resimleri (Birden fazla seçebilirsiniz)</label>
                        <input type="file" accept="image/*" multiple onChange={(e) => setEkstraResim(Array.from(e.target.files))} />
                    </div>


                    <div className="product-form__field">
                        <label>Ana Kategori</label>
                        <select
                            value={seciliAnaKategori}
                            onChange={(e) => {
                                setSeciliAnaKategori(e.target.value);
                                setSeciliAltKategori('');
                                setSeciliEnAltKategori('');
                                setDinamikDegerler({});
                            }}
                            required
                        >
                            <option value="">Lütfen Ana Kategori Seçin</option>
                            {kategoriler.map(cat => (
                                <option key={cat.id} value={cat.id}>{cat.name}</option>
                            ))}
                        </select>
                    </div>

                    {aktifAltKategoriler.length > 0 && (
                        <div className="product-form__field">
                            <label>Alt Kategori</label>
                            <select
                                value={seciliAltKategori}
                                onChange={(e) => {
                                    setSeciliAltKategori(e.target.value);
                                    setSeciliEnAltKategori('');
                                    setDinamikDegerler({});
                                }}
                            >
                                <option value="">Alt Kategori Seçin</option>
                                {aktifAltKategoriler.map(sub => (
                                    <option key={sub.id} value={sub.id}>{sub.name}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {aktifEnAltKategoriler.length > 0 && (
                        <div className="product-form__field">
                            <label>Ürün Tipi</label>
                            <select
                                value={seciliEnAltKategori}
                                onChange={(e) => {
                                    setSeciliEnAltKategori(e.target.value);
                                    setDinamikDegerler({});
                                }}
                            >
                                <option value="">Ürün Tipi Seçin</option>
                                {aktifEnAltKategoriler.map(subSub => (
                                    <option key={subSub.id} value={subSub.id}>{subSub.name}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {toplananOzellikler.length > 0 && (
                        <div className="product-form__dynamic-fields" style={{ marginTop: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
                            <h3 style={{ marginBottom: '15px' }}>Kategoriye Özel Nitelikler</h3>
                            {toplananOzellikler.map(ozellik => (
                                <div key={ozellik.id} className="product-form__field">
                                    <label>{ozellik.isim}</label>

                                    {ozellik.filtre_tipi === 'secim' ? (
                                        <select
                                            value={dinamikDegerler[ozellik.id] || ''}
                                            onChange={(e) => setDinamikDegerler(prev => ({ ...prev, [ozellik.id]: e.target.value }))}
                                            required
                                        >
                                            <option value="">Lütfen Seçiniz</option>
                                            {ozellik.secenekler && ozellik.secenekler.split(',').map((secenek, index) => (
                                                <option key={index} value={secenek.trim()}>
                                                    {secenek.trim()}
                                                </option>
                                            ))}
                                        </select>
                                    ) :

                                        ozellik.filtre_tipi === 'boolean' ? (
                                            <select
                                                value={dinamikDegerler[ozellik.id] || ''}
                                                onChange={(e) => setDinamikDegerler(prev => ({ ...prev, [ozellik.id]: e.target.value }))}
                                                required
                                            >
                                                <option value="">Seçiniz</option>
                                                <option value="Evet">Evet</option>
                                                <option value="Hayır">Hayır</option>
                                            </select>
                                        ) :

                                            (
                                                <input
                                                    type="text"
                                                    value={dinamikDegerler[ozellik.id] || ''}
                                                    onChange={(e) => setDinamikDegerler(prev => ({ ...prev, [ozellik.id]: e.target.value }))}
                                                    placeholder={`${ozellik.isim} giriniz...`}
                                                    required
                                                />
                                            )}
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="product-form__common-filters" style={{ marginTop: '20px', padding: '15px', background: '#f9f9f9', borderRadius: '8px' }}>
                        <h3 style={{ marginBottom: '15px', fontSize: '16px' }}>Ekstra Özellikler</h3>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isBulkSale} onChange={(e) => setIsBulkSale(e.target.checked)} /> Toplu Satışa Uygun
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isGiftWrap} onChange={(e) => setIsGiftWrap(e.target.checked)} /> Hediye Paketi
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={hasVideo} onChange={(e) => setHasVideo(e.target.checked)} /> Videolu Ürün
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isCampaign} onChange={(e) => setIsCampaign(e.target.checked)} /> Kampanyalı Ürün
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isBuyTogether} onChange={(e) => setIsBuyTogether(e.target.checked)} /> Birlikte Al Kazan
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isBuyMorePayLess} onChange={(e) => setIsBuyMorePayLess(e.target.checked)} /> Çok Al Az Öde
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isCorporateInvoice} onChange={(e) => setIsCorporateInvoice(e.target.checked)} /> Kurumsal Fatura
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 'normal' }}>
                                <input type="checkbox" checked={isEditorChoice} onChange={(e) => setIsEditorChoice(e.target.checked)} /> Fenomen Seçimi
                            </label>
                        </div>
                    </div>

                    <button type="submit" className="product-form__submit" style={{ marginTop: '20px' }}>Ürün Oluştur</button>
                </form>
            </div>
        </div>
    )
}

export default UrunOlustur