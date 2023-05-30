# Analytics Portal Backend (Payload)

---

## Login App

---

#### Login API

POST `/api/token/`

**Request:**

```json
{
 "email"     :   "admin@redingtongulf.com",
 "password"  :   "administrator"
}
```

**Response:**

```json
{
 "token"    :    "x1sfgrl?19seQDsx.&!sw",
 "isAdmin"  :    1,
 "name"     :    "Administrator"
}
```

**Errors:**

- `401` : If user unauthorized

## Management App

---

#### Tabel API

GET `/mdm/table/`

**Request:**

```json
{
    "token"  :   "x1sfgrl?19seQDsx.&!sw"
}
```

#### History API

GET `/mdm/history/`

**Request:**

```json
{
    "token"  :   "x1sfgrl?19seQDsx.&!sw"
}
```

#### KPIs API

GET `/mdm/kpi/`

**Request:**

```json
{
    "token"  :   "x1sfgrl?19seQDsx.&!sw"
}
```
