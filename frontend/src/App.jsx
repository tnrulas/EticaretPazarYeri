import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Sepet from '../src/pages/Cart'
import Odeme from '../src/pages/Checkout'
import Anasayfa from '../src/pages/Home'
import Giris from '../src/pages/Login'
import OdemeBasarili from '../src/pages/OrderSuccess'
import UrunOlusturSayfasi from '../src/pages/ProductCreatePage'
import UrunSayfasi from '../src/pages/ProductPage'
import Kayit from '../src/pages/Register'
import ProtectedRoute from '../src/components/ProtectedRoute'
import SearchThings from '../src/pages/SearchPage'
import Categories from '../src/pages/CategoryPage'



function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path='/'
          element={
            <Anasayfa />
          }
        />
        <Route
          path='/giris'
          element={
            <Giris />
          }
        />
        <Route
          path='/kayit'
          element={
            <Kayit />
          }
        />
        <Route
          path='/urunOlustur'
          element={
            <ProtectedRoute>
              <UrunOlusturSayfasi />
            </ProtectedRoute>

          }
        />
        <Route
          path='/urunSayfasi/:id'
          element={
            <UrunSayfasi />
          }
        />
        <Route
          path='/sepet'
          element={
            <ProtectedRoute>
              <Sepet />
            </ProtectedRoute>
          }
        />
        <Route
          path='/odeme'
          element={
            <ProtectedRoute>
              <Odeme />
            </ProtectedRoute>
          }
        />
        <Route
          path='/odemeBasarili'
          element={
            <ProtectedRoute>
              <OdemeBasarili />
            </ProtectedRoute>
          }
        />
        <Route
          path='/search'
          element={
            <SearchThings />
          }
        />
        <Route
          path='/filter'
          element={
            <Categories />
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
