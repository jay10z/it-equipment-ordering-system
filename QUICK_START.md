# 🚀 Quick Start Guide - ProTech Solutions

## Get Started in 3 Steps

### Step 1: Open the Website
```
Navigate to: src/index.html
Double-click to open in your browser
```

### Step 2: Explore the Features
- **Home**: See the hero section and featured products
- **Products**: Browse all 12 IT products with category filters
- **Cart**: Add items and manage your shopping cart
- **Login/Register**: Try the authentication forms
- **Contact**: Fill out the contact form
- **About**: Learn about ProTech Solutions

### Step 3: Customize (Optional)
Edit these files to personalize:
- `src/scripts/products.js` - Add/edit products
- Footer sections in each HTML file - Update contact info
- `src/styles/main.css` - Adjust colors

---

## 📱 Features to Test

### Shopping Experience
1. Go to **Products** page
2. Click a category filter (e.g., "Networking Equipment")
3. Click **"Add to Cart"** on any product
4. Click **"Cart"** in navigation
5. Adjust quantities with +/- buttons

### Form Validation
1. Go to **Register** page
2. Try submitting empty form (error appears)
3. Enter invalid email (validation triggers)
4. Enter 5-digit phone (must be 9 digits starting with 6)

### Navigation
- All links in header work
- Footer links navigate correctly
- Shopping cart persists across pages

---

## 🎨 Color Scheme Reference

If you want to customize colors, edit `src/styles/main.css`:

```css
:root {
    --primary-color: #0a192f;      /* Dark blue background */
    --secondary-color: #112240;     /* Card backgrounds */
    --accent-color: #64ffda;        /* Buttons, links */
    --text-primary: #e6f1ff;        /* Main text */
    --text-secondary: #8892b0;      /* Secondary text */
}
```

---

## 📦 Products Included

**12 Sample Products:**
- 3 Laptops (Dell, HP, Lenovo)
- 3 Networking devices (Router, Switch, Access Point)
- 3 Accessories (Mouse, Keyboard, Cable)
- 3 Storage devices (HDD, SSD, USB)

**To add more products**, edit `src/scripts/products.js`:
```javascript
{
    id: 13,
    name: 'Your Product Name',
    category: 'Computers' // or 'Networking', 'Accessories', 'Storage'
    price: 50000,  // in FCFA
    availability: 'In Stock',
    warranty: '12 months',
    specs: 'Product specifications here'
}
```

---

## ⚡ Quick Fixes

### Products not showing?
- Check browser console (F12) for JavaScript errors
- Ensure `scripts/products.js` is loaded

### Styles look broken?
- Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)
- Check that CSS files are in `src/styles/` folder

### Cart not saving?
- Ensure localStorage is enabled in browser
- Check browser privacy settings

---

## 🌐 For Deployment

When ready to deploy online:

1. **Host the files**: Upload `/src` folder to web hosting
2. **Domain**: Point your domain to the hosting
3. **SSL**: Enable HTTPS for security
4. **Backend**: Add server for user accounts and real transactions

**Recommended hosts for Cameroon:**
- For testing: GitHub Pages (free)
- For production: Local hosting providers

---

## 📞 Need Help?

- **Full documentation**: See `README.md`
- **Transformation details**: See `TRANSFORMATION_SUMMARY.md`
- **Code comments**: Check JavaScript files for inline explanations

---

## ✅ Checklist Before Presenting

- [ ] Open `index.html` - Hero section displays correctly
- [ ] Navigate to Products - All 12 products appear
- [ ] Test category filters - Products filter correctly
- [ ] Add item to cart - Cart icon/link works
- [ ] View cart - Items display with quantities
- [ ] Test login form - Validation messages appear
- [ ] Test register form - Phone/email validation works
- [ ] Check contact page - Form looks professional
- [ ] View aboutpage - Company info displays
- [ ] Test mobile view - Responsive layout works

---

**You're all set! Open `src/index.html` and start exploring!** 🎉
