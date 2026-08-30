# Screen: Product Detail Screen
# Figma Screenshot: ../screenshots/product_detail_screen.png

---

## Event: `add_to_cart_clicked`
- **Trigger:** Kullanıcı "Add to Cart" butonuna tıkladığında tetiklenir.
- **Source Data Sample:** `../mock_data/product_detail_response.json`
- **Destinations:** `firebase`, `adjust`, `sgtm`

### Parameter Mapping Rules
| Target Event Param (SDK) | Source Path (JSON Response) | Data Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | `$.productId` | String | Yes | Eklenen ürünün ID'si |
| `product_name` | `$.title` | String | Yes | Ürünün adı |
| `unit_price` | `$.price` | Double | Yes | Ürün birim fiyatı |
| `category` | `$.category` | String | No | Ürün kategorisi |


