import React from 'react'
import Navbar from '../components/Navbar'
import SearchAll from '../components/CategoryList'
import CategoryLists from '../components/CategoryList'
import Footers from '../components/Footer'

function Categories() {
    return (
        <div>
            <Navbar />
            <CategoryLists />
            <Footers />
        </div>
    )
}

export default Categories