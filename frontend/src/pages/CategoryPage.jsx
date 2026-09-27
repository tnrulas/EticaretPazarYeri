import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import SearchAll from '../components/CategoryList'
import CategoryLists from '../components/CategoryList'
import Footers from '../components/Footer'
import Filter from '../components/Filters'
import '../style/filters.css'

function Categories() {
    const [products, setProducts] = useState([])

    return (
        <div>
            <Navbar />
            <div className="page-layout">
                <Filter products={products} setProducts={setProducts} />
                <div className="page-content">
                    <CategoryLists products={products} setProducts={setProducts} />
                </div>
            </div>
            <Footers />
        </div>
    )
}

export default Categories