import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import SearchAll from '../components/Search'
import Footers from '../components/Footer'
import Filter from '../components/Filters'
import '../style/filters.css'


function SearchThings() {
    const [products2, setProducts2] = useState([])
    return (
        <div>
            <Navbar />
            <div className="page-layout">
                <Filter products={products2} setProducts={setProducts2} />
                <div className="page-content">
                    <SearchAll products2={products2} setProducts2={setProducts2} />
                </div>
            </div>
            <Footers />
        </div>
    )
}

export default SearchThings