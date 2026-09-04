# API 文档

## 1. 基础约定

- **Base URL**: `http://<host>:8000/api/v1`
- **数据格式**: 请求体与响应体均为 `application/json`(登录接口使用 `application/x-www-form-urlencoded`)
- **鉴权方式**: Bearer Token需要登录的接口在请求头携带: 

```http
Authorization: Bearer <access_token>
```

- 交互式文档: `http://<host>:8000/docs`(Swagger UI)

### 1.1 统一响应结构

所有业务接口统一返回如下结构: 

```json
{
  "code": 200,
  "message": "success",
  "data": { }
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 状态码，成功为 `200`; 失败与 HTTP 状态码一致 |
| message | string | 提示信息，成功默认 `success`，失败为具体错误描述 |
| data | any | 业务数据，无数据时为 `null` |

### 1.2 错误码

| HTTP 状态码 | 含义 |
| --- | --- |
| 400 | 业务校验失败 / 参数有误 |
| 401 | 未认证或凭证失效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 422 | 请求参数校验失败 |
| 500 | 服务器内部错误 |

错误响应示例: 

```json
{
  "code": 400,
  "message": "用户名已存在",
  "data": null
}
```

## 2. 认证模块 `/auth`

### 2.1 用户注册

`POST /auth/register`

请求体: 

```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "password": "Abc12345",
  "password_confirm": "Abc12345"
}
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| username | string | 是 | 字母开头，3-50 位字母/数字/下划线 |
| email | string | 是 | 合法邮箱 |
| phone | string | 否 | 11 位手机号 |
| password | string | 是 | 8-20 位，含大小写字母与数字 |
| password_confirm | string | 是 | 需与 password 一致 |

成功响应 `data`(用户信息): 

```json
{
  "user_id": 1,
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "phone": "13800138000",
  "balance": 1000.0,
  "role": "user",
  "created_at": "2026-01-01T00:00:00"
}
```

### 2.2 用户登录

`POST /auth/login`

请求体(form-urlencoded): 

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

成功响应 `data`: 

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### 2.3 刷新访问令牌

`POST /auth/refresh`

请求体: 

```json
{ "refresh_token": "eyJ..." }
```

成功响应 `data`: 

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### 2.4 获取当前用户信息

`GET /auth/me`(需登录)

成功响应 `data`: 同「用户注册」中的用户信息结构

## 3. 用户模块 `/users`

> 以下接口均需登录(Bearer Token)

### 3.1 更新当前用户信息

`PUT /users/me`

请求体(字段均为可选): 

```json
{ "email": "new@example.com", "phone": "13900139000" }
```

成功响应 `data`: 更新后的用户信息

### 3.2 修改密码

`PUT /users/me/password`

请求体: 

```json
{ "old_password": "Abc12345", "new_password": "Xyz98765" }
```

成功响应: `data` 为 `null`，`message` 为 `密码修改成功`

### 3.3 查询余额

`GET /users/me/balance`

成功响应 `data`: 

```json
{ "balance": 1000.0, "currency": "CNY" }
```

### 3.4 账户充值

`POST /users/me/recharge`

请求体: 

```json
{ "amount": 500 }
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| amount | number | 是 | 充值金额，必须大于 0 |

成功响应 `data`: 

```json
{ "balance": 1500.0, "currency": "CNY" }
```

## 4. 商品模块 `/products`

### 4.1 商品列表(分页)

`GET /products`

查询参数: 

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| page | int | 1 | 页码，>=1 |
| page_size | int | 10 | 每页数量，1-100 |

成功响应 `data`: 

```json
{
  "items": [ { "product_id": 1, "name": "iPhone 17 Pro", "price": 9999.0, "stock": 100, "image_url": "/static/upload/xxx.jpg", "is_active": true, "description": "..." } ],
  "total": 100,
  "page": 1,
  "page_size": 10
}
```

### 4.2 商品搜索

`GET /products/search`

查询参数: `keyword`(必填)、`page`、`page_size`响应 `data` 结构同「商品列表」

### 4.3 商品详情

`GET /products/{product_id}`

成功响应 `data`: 单个商品对象(结构见 4.1 中 `items` 元素)

### 4.4 创建商品(管理员)

`POST /products`(需管理员)

请求体: 

```json
{
  "name": "MacBook Air",
  "description": "M4 芯片",
  "price": 9499.0,
  "stock": 50,
  "image_url": "/static/upload/macbook_air_display.jpg"
}
```

成功响应 `data`: 新建的商品对象

### 4.5 更新商品(管理员)

`PUT /products/{product_id}`(需管理员)

请求体字段均可选(`name` / `description` / `price` / `stock` / `image_url` / `is_active`)，仅更新传入字段成功响应 `data`: 更新后的商品对象

### 4.6 删除商品(管理员)

`DELETE /products/{product_id}`(需管理员)

软删除(将 `is_active` 置为 `false`)成功响应: `data` 为 `null`，`message` 为 `删除成功`

## 5. 购物车模块 `/cart`

> 以下接口均需登录(Bearer Token)

### 5.1 查看购物车

`GET /cart`

成功响应 `data`: 

```json
{
  "items": [
    {
      "cart_item_id": 1,
      "product_id": 1,
      "product_name": "iPhone 17 Pro",
      "product_price": 9999.0,
      "quantity": 2,
      "subtotal": 19998.0,
      "created_at": "2026-01-01T00:00:00",
      "image_url": "/static/upload/xxx.jpg"
    }
  ],
  "total_amount": 19998.0,
  "total_quantity": 2
}
```

### 5.2 添加商品到购物车

`POST /cart/items`

请求体: 

```json
{ "product_id": 1, "quantity": 2 }
```

成功响应 `data`: 更新后的购物车结构(同 5.1)

### 5.3 更新购物车商品数量

`PUT /cart/items/{product_id}`

请求体: 

```json
{ "quantity": 3 }
```

成功响应 `data`: 更新后的购物车结构

### 5.4 删除购物车商品

`DELETE /cart/items/{product_id}`

成功响应 `data`: 更新后的购物车结构

### 5.5 清空购物车

`DELETE /cart/clear`

成功响应 `data`: 清空后的购物车结构(`items` 为空)

### 5.6 结算

`POST /cart/checkout`

校验库存与余额，扣减库存和余额并清空购物车成功响应 `data`: 

```json
{ "success": true, "total_amount": 19998.0, "message": "结算成功" }
```

常见失败: 库存不足(400)、余额不足(400)、购物车为空(400)

## 6. 数据模型速查

### UserResponse

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| user_id | int | 用户 ID |
| username | string | 用户名 |
| email | string | 邮箱 |
| phone | string\|null | 手机号 |
| balance | number | 账户余额 |
| role | string | `user` / `admin` |
| created_at | string | 注册时间 |

### ProductResponse

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| product_id | int | 商品 ID |
| name | string | 商品名称 |
| description | string\|null | 商品描述 |
| price | number | 价格 |
| stock | int | 库存 |
| image_url | string\|null | 图片 URL |
| is_active | bool | 是否上架 |
| created_at / updated_at | string | 时间戳 |
