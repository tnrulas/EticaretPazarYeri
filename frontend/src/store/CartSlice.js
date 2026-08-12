import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    cartItems: [],
}

const cartSlice = createSlice({
    name: 'cart',
    initialState,
    reducers: {
        addToCart: (state, action) => {
            const ProductAdd = action.payload;

            const existingItem = state.cartItems.find(item => item.id === ProductAdd.id);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                state.cartItems.push({
                    product: ProductAdd,
                    quantity: 1,
                    buyer: localStorage.getItem('username')
                });
            }

        }
    }
});

export const { addToCart } = cartSlice.actions;

export default cartSlice.reducer;