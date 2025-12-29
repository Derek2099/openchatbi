# AE Domain (Adverse Events) - 不良事件域

## 域概述
**用途**: 记录所有不良事件  
**特点**: 每个受试者可有多条 AE 记录  
**类型**: 事件域（Events Domain）

---

## 核心变量

### 标识符变量
- **STUDYID** - 研究标识符
- **DOMAIN** - 域代码 ('AE')
- **USUBJID** - 唯一受试者ID
- **AESEQ** - 不良事件序号

### 事件描述变量
- **AETERM** - 不良事件报告术语（原始术语）
- **AEDECOD** - 不良事件编码术语（字典编码，如 MedDRA）
- **AEBODSYS** - 身体系统/器官分类

### 严重性变量
- **AESER** - 严重不良事件标志
  - 'Y' = 是 SAE（Serious Adverse Event）
  - 'N' = 否
  - **SAE 定义**: 导致死亡、危及生命、需要住院、导致残疾等
- **AESEV** - 严重程度
  - 'MILD' = 轻度
  - 'MODERATE' = 中度
  - 'SEVERE' = 重度

### 因果关系变量
- **AEREL** - 与研究药物的因果关系
  - 'RELATED' = 相关
  - 'NOT RELATED' = 不相关
  - 'POSSIBLY RELATED' = 可能相关
  - 'PROBABLY RELATED' = 很可能相关

### 结局变量
- **AEOUT** - 不良事件结局
  - 'RECOVERED/RESOLVED' = 恢复/消退
  - 'RECOVERING/RESOLVING' = 恢复中
  - 'NOT RECOVERED/NOT RESOLVED' = 未恢复
  - 'FATAL' = 致死
  - 'UNKNOWN' = 未知

### 动作变量
- **AEACN** - 对研究药物采取的措施
  - 'DOSE NOT CHANGED' = 剂量不变
  - 'DOSE REDUCED' = 剂量减少
  - 'DRUG WITHDRAWN' = 药物撤回
  - 'NOT APPLICABLE' = 不适用

### 日期变量
- **AESTDTC** - 不良事件开始日期时间（ISO 8601）
- **AEENDTC** - 不良事件结束日期时间（ISO 8601）
- **AESTDY** - 相对研究开始的天数
- **AEENDY** - 相对研究结束的天数

---

## 业务规则

1. **多重性**: 一个受试者可有多条 AE 记录
2. **关联**: 通过 USUBJID 关联到 DM 域
3. **SAE 标识**: AESER='Y' 标识严重不良事件
4. **日期完整性**: AESTDTC 必填，AEENDTC 可选（事件可能持续中）

---

## 常见查询模式

### 1. AE 总数
```sql
SELECT COUNT(*) as ae_count FROM ae
```

### 2. 受试者 AE 发生率
```sql
SELECT 
    dm.ARM,
    COUNT(DISTINCT CASE WHEN ae.USUBJID IS NOT NULL THEN dm.USUBJID END) * 100.0 / COUNT(DISTINCT dm.USUBJID) as ae_rate
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
GROUP BY dm.ARM
```

### 3. SAE 发生率（重要指标）
```sql
SELECT 
    dm.ARM,
    COUNT(DISTINCT CASE WHEN ae.AESER='Y' THEN dm.USUBJID END) * 100.0 / COUNT(DISTINCT dm.USUBJID) as sae_rate,
    COUNT(DISTINCT CASE WHEN ae.AESER='Y' THEN dm.USUBJID END) as sae_subjects,
    COUNT(DISTINCT dm.USUBJID) as total_subjects
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
GROUP BY dm.ARM
```

### 4. 按严重程度统计
```sql
SELECT 
    AESEV,
    COUNT(*) as ae_count,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
GROUP BY AESEV
ORDER BY 
    CASE AESEV
        WHEN 'SEVERE' THEN 1
        WHEN 'MODERATE' THEN 2
        WHEN 'MILD' THEN 3
    END
```

### 5. 按身体系统统计
```sql
SELECT 
    AEBODSYS,
    COUNT(*) as ae_count,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
GROUP BY AEBODSYS
ORDER BY ae_count DESC
```

### 6. 最常见的 AE（Top 10）
```sql
SELECT 
    AEDECOD,
    COUNT(*) as occurrence,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
GROUP BY AEDECOD
ORDER BY occurrence DESC
LIMIT 10
```

### 7. 治疗组间 SAE 对比
```sql
SELECT 
    dm.ARM,
    ae.AEDECOD,
    COUNT(*) as sae_count
FROM dm
INNER JOIN ae ON dm.USUBJID = ae.USUBJID
WHERE ae.AESER = 'Y'
GROUP BY dm.ARM, ae.AEDECOD
ORDER BY dm.ARM, sae_count DESC
```

---

## 表选择规则

### 何时使用 AE 域
- ✅ 查询包含 "不良事件"、"AE"
- ✅ 查询包含 "严重不良事件"、"SAE"
- ✅ 查询 "安全性"、"耐受性"
- ✅ 查询特定症状或事件

### 何时 JOIN DM 域
- ✅ 需要治疗组信息（ARM）
- ✅ 需要人口统计学信息（年龄、性别）
- ✅ 计算发生率（需要总受试者数）

---

## SQL 生成注意事项

1. **SAE 识别**: 使用 `WHERE AESER='Y'`
2. **发生率计算**: 需要 JOIN DM 获取总受试者数
3. **去重**: 使用 `COUNT(DISTINCT USUBJID)` 计算受试者数
4. **日期比较**: 使用 AESTDTC、AEENDTC（ISO 8601 格式）
5. **NULL 处理**: AEENDTC 可能为 NULL（事件持续中）

---

## 数据质量检查

- ✅ USUBJID 存在于 DM
- ✅ AESER 值域（Y/N）
- ✅ AESEV 值域（MILD/MODERATE/SEVERE）
- ✅ 日期格式 ISO 8601
- ✅ AESTDTC <= AEENDTC（如果结束日期存在）
