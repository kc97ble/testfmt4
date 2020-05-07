# /upload

## 200

```
{
  uploaded_file_id: "ad96145a-0db7-41c5-a0f1-c1010d7fb3ee"
}
```

# /preview

## Parameters

```
{
  uploaded_file_id: String,
  before_format: {
    inp: { format: String }
    out: { format: String }
  },
  after_format: {
    inp: { format: String }
    out: { format: String }
  }
}
```

## 200

```
{
  before: [
    path: String,
    important: boolean
  ],
  after: [
    path: String,
    important: boolean
  ]
}
```

# /download

## Parameters

```
{
  uploaded_file_id: String,
  before_format: {
    inp: { format: String }
    out: { format: String }
  },
  after_format: {
    inp: { format: String }
    out: { format: String }
  },
  file_name: String
}
```

## 200

The formatted test suite
