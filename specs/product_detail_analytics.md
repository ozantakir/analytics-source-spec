# Product Detail Analytics Spec

## Event: Add To Cart Clicked
- **Event Name:** `add_to_cart_clicked`
- **Description:** Kullanıcı ürün detay ekranında sepeti ekle butonuna bastığında tetiklenir.
- **Destinations:** `FIREBASE`, `ADJUST`, `INSIDER`

### Parametreler & Mapping Tablosu

| Parametre İsmi | Tipi | Zorunlu | Açıklama | Firebase Key | Adjust Key | Insider Key |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `productId` | String | Evet | Ürün ID bilgisi | `item_id` | *-* | `product_id` |
| `price` | Double | Evet | Ürün birim fiyatı | `value` | `revenue` | `price` |
| `quantity` | Int | Evet | Eklenen adet | `quantity` | *-* | `quantity` |
| `category` | String | Hayır | Ürün kategorisi | `item_category` | *-* | `category` |
