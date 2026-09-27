import React from "react"
import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import api from "../services/api"


function Filter({ products, setProducts }) {
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [kategori, setKategori] = useState(null);
    const [kategoriler, setKategoriler] = useState([]);
    const [filtreler, setFiltreler] = useState([]);
    const [searchParams] = useSearchParams();
    const [sabitFiltre, setSabitFiltre] = useState([]);

    const [seciliGenelFiltreler, setSeciliGenelFiltreler] = useState([]);
    const [seciliOzelFiltreler, setSeciliOzelFiltreler] = useState([]);

    const categoryId = searchParams.get('category');
    const categoryName = searchParams.get('name') || '';
    const query = searchParams.get('q') || '';

    useEffect(() => {
        if (query) {
            setKategori(query);
        } else if (categoryName) {
            setKategori(categoryName);
        } else {
            setKategori(null)
        }

    }, [query, categoryName]);

    useEffect(() => {
        const fetchKategoriler = async () => {
            try {
                const response = await api.get('urunler/kategoriler/');
                setKategoriler(response.data);

                // if (kategoriler) {
                //     for (let sayi = 0; sayi <= kategoriler.length; sayi++) {
                //         if (kategoriler[sayi] === kategori) {
                //             setSelectedCategory(kategoriler[sayi])
                //         } else {
                //             continue;
                //         }
                //     }
                // }
            } catch (error) {
                console.log("kategorileri çekerken bir hata oluştu", error);
            }
        }
        fetchKategoriler();
    }, [])

    useEffect(() => {
        if (!kategori || kategoriler.length === 0) {
            setSelectedCategory(null);
            setFiltreler([]);
            return;
        }

        const aranan = kategori.toLocaleLowerCase('tr');
        const stack = kategoriler.map((k) => ({ kat: k, ustFiltreler: [] }));

        while (stack.length > 0) {
            const { kat, ustFiltreler } = stack.pop();
            const tumFiltreler = [...ustFiltreler, ...kat.ozellikler];

            const eslesti = categoryId
                ? String(kat.id) === categoryId
                : kat.name.toLocaleLowerCase('tr') === aranan;

            if (eslesti) {
                setSelectedCategory(kat);
                setFiltreler(tumFiltreler);
                return;
            }

            kat.subcategories.forEach((alt) =>
                stack.push({ kat: alt, ustFiltreler: tumFiltreler })
            );
        }
        setSelectedCategory(null);
        setFiltreler([]);
    }, [kategori, kategoriler, categoryId]);

    useEffect(() => {
        const fetchSabitFiltreler = async () => {
            try {
                const response = await api.get(`urunler/Urunliste/`);

                if (response.data && response.data.length > 0) {
                    const ilkUrun = response.data[0];

                    const aranacakAlanlar = [
                        'is_bulk_sale', 'is_gift_wrap', 'has_video',
                        'is_campaign', 'is_buy_together', 'is_buy_more_pay_less',
                        'is_corporate_invoice', 'is_editor_choice'
                    ];

                    const dinamikSabitFiltreler = aranacakAlanlar.filter(alan => alan in ilkUrun);

                    setSabitFiltre(dinamikSabitFiltreler);
                    console.log(sabitFiltre)
                }
            } catch (error) {
                console.error("Filtreler çekilirken hata oluştu:", error);
            }
        }
        fetchSabitFiltreler();
    }, []);

    const sabitFiltrele = (f) => {
        try {
            setSeciliGenelFiltreler((prev) => {
                if (prev.includes(f)) {
                    return prev.filter((item) => item !== f);
                } else {
                    return [...prev, f];
                }
            });

        } catch (error) {
            console.log("eeeeeeeee", f)
        }

    }

    const ozelFiltrele = (isim, deger) => {
        const kombinasyon = `${isim}:${deger}`;
        try {
            setSeciliOzelFiltreler((prev) => {
                if (prev.includes(kombinasyon)) {
                    return prev.filter((item) => item !== kombinasyon);
                } else {
                    return [...prev, kombinasyon];
                }
            });
        } catch (error) {
            console.log("eeeeeeeee", kombinasyon)
        }
    }

    const filtreyiGönder = async () => {
        try {
            const response = await api.get('urunler/filtrele/', {
                params: {
                    genel: seciliGenelFiltreler,
                    ozel: seciliOzelFiltreler,
                    category: categoryId,
                    q: query
                },
                paramsSerializer: {
                    indexes: null
                }
            })
            setProducts(response.data)
        } catch (error) {
            console.error("Ürünler çekilirken hata oluştu:", error)
        }
    }

    return (
        <div className="filter-panel">
            {sabitFiltre.length > 0 && (
                <div className="filter-section">
                    <h4 className="filter-section-title">Genel Filtreler</h4>
                    <ul className="filter-list">
                        {sabitFiltre.map((f) => (
                            <li key={f} className="filter-item">
                                <label className="filter-checkbox-label">
                                    <input type="checkbox" onClick={() => {
                                        sabitFiltrele(f)
                                    }} />
                                    <span>{f}</span>
                                </label>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {filtreler.length > 0 && (
                <div className="filter-section">
                    <h4 className="filter-section-title">Kategoriye Özel Filtreler</h4>
                    <ul className="filter-list">
                        {filtreler.map((f) => (
                            <li key={f.id} className="filter-item">
                                <strong className="filter-name">{f.isim}</strong>
                                {f.filtre_tipi === 'boolean' && (
                                    <label className="filter-checkbox-label">
                                        <input type="checkbox" onClick={() => {
                                            ozelFiltrele(f.isim, "Evet")
                                        }} />
                                        <span>Evet</span>
                                    </label>
                                )}
                                {f.filtre_tipi === 'secim' && f.secenekler && (
                                    <ul className="filter-options">
                                        {f.secenekler.split(',').map((s) => (
                                            <li key={s}>
                                                <label className="filter-checkbox-label">
                                                    <input type="checkbox" onClick={() => {
                                                        ozelFiltrele(f.isim, s.trim())
                                                    }} />
                                                    <span>{s.trim()}</span>
                                                </label>
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            <button onClick={filtreyiGönder}> SEÇİMLERİ FİLTRELE</button>
        </div>
    )
}

export default Filter;