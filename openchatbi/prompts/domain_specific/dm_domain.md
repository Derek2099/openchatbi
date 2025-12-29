# DM Domain (Demographics) - 人口统计学域

## 域概述
**用途**: 存储受试者的基本信息  
**特点**: 每个受试者一条记录，所有其他域的关联基础  
**类型**: 特殊用途域（Special Purpose Domain）

---

## 核心变量

### 标识符变量
- **STUDYID** - 研究标识符
- **DOMAIN** - 域代码 ('DM')
- **USUBJID** - 唯一受试者ID（格式: STUDYID-SITEID-SUBJID）
- **SUBJID** - 受试者编号
- **SITEID** - 研究中心ID

### 人口统计学变量
- **AGE** - 年龄（数值）
- **AGEU** - 年龄单位（通常为 'YEARS'）
- **SEX** - 性别
  - 'M' = 男性 (Male)
  - 'F' = 女性 (Female)
  - 'U' = 未知 (Unknown)
- **RACE** - 种族
- **ETHNIC** - 民族
- **COUNTRY** - 国家

### 治疗组变量
- **ARM** - 计划治疗组名称
- **ARMCD** - 计划治疗组代码（如 'TRT', 'PLB'）
- **ACTARM** - 实际治疗组名称
- **ACTARMCD** - 实际治疗组代码

### 日期变量
- **RFSTDTC** - 首次研究治疗日期（Reference Start Date）
- **RFENDTC** - 最后研究治疗日期（Reference End Date）
- **RFXSTDTC** - 首次研究药物日期
- **RFXENDTC** - 最后研究药物日期

---

## 业务规则

1. **唯一性**: 每个受试者有且仅有一条 DM 记录
2. **主键**: USUBJID 是唯一标识符
3. **关联基础**: 所有其他域通过 USUBJID 关联到 DM
4. **完整性**: DM 必须包含研究中所有受试者

---

## 常见查询模式

### 1. 受试者总数
```sql
SELECT COUNT(DISTINCT USUBJID) as subject_count FROM dm
```

### 2. 各治疗组受试者数
```sql
SELECT ARM, COUNT(*) as subject_count
FROM dm
GROUP BY ARM
ORDER BY subject_count DESC
```

### 3. 年龄统计
```sql
SELECT 
    ARM,
    AVG(AGE) as mean_age,
    MIN(AGE) as min_age,
    MAX(AGE) as max_age,
    STDDEV(AGE) as std_age
FROM dm
GROUP BY ARM
```

### 4. 性别分布
```sql
SELECT 
    ARM,
    SEX,
    COUNT(*) as count
FROM dm
GROUP BY ARM, SEX
```

### 5. 年龄组分布
```sql
SELECT 
    CASE 
        WHEN AGE < 18 THEN '< 18 years'
        WHEN AGE BETWEEN 18 AND 65 THEN '18-65 years'
        ELSE '> 65 years'
    END as age_group,
    COUNT(*) as subject_count
FROM dm
GROUP BY age_group
```

---

## 数据质量检查

- ✅ USUBJID 唯一性
- ✅ AGE 合理范围（0-120）
- ✅ SEX 值域检查（M/F/U）
- ✅ ARM 和 ARMCD 对应关系
- ✅ 日期格式 ISO 8601
