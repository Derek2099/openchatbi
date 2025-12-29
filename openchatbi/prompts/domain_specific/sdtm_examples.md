# CDISC SDTM IG 3.4 查询示例

本文档提供常见临床试验数据分析查询的示例，用于训练和指导 SQL 生成。

---

## 1. 人口统计学分析（DM 域）

### 示例 1.1：受试者总数
**用户问题**: "有多少名受试者参与了研究？"
**SQL**:
```sql
SELECT COUNT(DISTINCT USUBJID) as subject_count
FROM dm
```

### 示例 1.2：各治疗组受试者数
**用户问题**: "各治疗组分别有多少受试者？"
**SQL**:
```sql
SELECT ARM, COUNT(*) as subject_count
FROM dm
GROUP BY ARM
ORDER BY subject_count DESC
```

### 示例 1.3：年龄分布统计
**用户问题**: "受试者的年龄分布如何？"
**SQL**:
```sql
SELECT 
    MIN(AGE) as min_age,
    MAX(AGE) as max_age,
    AVG(AGE) as mean_age,
    STDDEV(AGE) as std_age,
    MEDIAN(AGE) as median_age
FROM dm
```

### 示例 1.4：按年龄组统计
**用户问题**: "按年龄组（<18, 18-65, >65）统计受试者分布"
**SQL**:
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
ORDER BY age_group
```

### 示例 1.5：性别分布
**用户问题**: "男性和女性受试者各有多少？"
**SQL**:
```sql
SELECT 
    SEX,
    COUNT(*) as count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM dm
GROUP BY SEX
```

### 示例 1.6：各中心入组情况
**用户问题**: "各研究中心分别入组了多少受试者？"
**SQL**:
```sql
SELECT 
    SITEID,
    COUNT(*) as subject_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM dm
GROUP BY SITEID
ORDER BY subject_count DESC
```

---

## 2. 不良事件分析（AE 域）

### 示例 2.1：AE 总数
**用户问题**: "研究中共发生了多少例不良事件？"
**SQL**:
```sql
SELECT COUNT(*) as total_ae_count
FROM ae
```

### 示例 2.2：发生 AE 的受试者数
**用户问题**: "有多少受试者至少发生了一次不良事件？"
**SQL**:
```sql
SELECT COUNT(DISTINCT USUBJID) as subjects_with_ae
FROM ae
```

### 示例 2.3：AE 发生率
**用户问题**: "不良事件的发生率是多少？"
**SQL**:
```sql
SELECT 
    COUNT(DISTINCT ae.USUBJID) as subjects_with_ae,
    COUNT(DISTINCT dm.USUBJID) as total_subjects,
    COUNT(DISTINCT ae.USUBJID) * 100.0 / COUNT(DISTINCT dm.USUBJID) as ae_rate_percent
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
```

### 示例 2.4：各治疗组 AE 发生率对比
**用户问题**: "各治疗组的不良事件发生率分别是多少？"
**SQL**:
```sql
SELECT 
    dm.ARM,
    COUNT(DISTINCT dm.USUBJID) as total_subjects,
    COUNT(DISTINCT ae.USUBJID) as subjects_with_ae,
    COUNT(DISTINCT ae.USUBJID) * 100.0 / COUNT(DISTINCT dm.USUBJID) as ae_rate_percent
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
GROUP BY dm.ARM
ORDER BY ae_rate_percent DESC
```

### 示例 2.5：严重不良事件（SAE）统计
**用户问题**: "有多少例严重不良事件？"
**SQL**:
```sql
SELECT 
    COUNT(*) as total_sae,
    COUNT(DISTINCT USUBJID) as subjects_with_sae
FROM ae
WHERE AESER = 'Y'
```

### 示例 2.6：最常见的不良事件（Top 10）
**用户问题**: "最常见的 10 种不良事件是什么？"
**SQL**:
```sql
SELECT 
    AEDECOD as ae_term,
    COUNT(*) as ae_count,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
GROUP BY AEDECOD
ORDER BY ae_count DESC
LIMIT 10
```

### 示例 2.7：按严重程度分类的 AE
**用户问题**: "各严重程度的不良事件分别有多少例？"
**SQL**:
```sql
SELECT 
    AESEV as severity,
    COUNT(*) as ae_count,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
WHERE AESEV IS NOT NULL
GROUP BY AESEV
ORDER BY 
    CASE AESEV
        WHEN 'MILD' THEN 1
        WHEN 'MODERATE' THEN 2
        WHEN 'SEVERE' THEN 3
    END
```

### 示例 2.8：药物相关的 AE
**用户问题**: "有多少不良事件被认为与研究药物相关？"
**SQL**:
```sql
SELECT 
    AEREL as relationship,
    COUNT(*) as ae_count,
    COUNT(DISTINCT USUBJID) as subject_count
FROM ae
WHERE AEREL IN ('POSSIBLY RELATED', 'PROBABLY RELATED', 'RELATED')
GROUP BY AEREL
ORDER BY ae_count DESC
```

### 示例 2.9：特定 AE 的详细信息
**用户问题**: "显示所有头痛相关的不良事件"
**SQL**:
```sql
SELECT 
    ae.USUBJID,
    dm.AGE,
    dm.SEX,
    dm.ARM,
    ae.AETERM,
    ae.AESEV,
    ae.AESER,
    ae.AEREL,
    ae.AESTDTC
FROM ae
INNER JOIN dm ON ae.USUBJID = dm.USUBJID
WHERE ae.AEDECOD LIKE '%HEADACHE%'
ORDER BY ae.AESTDTC
```

### 示例 2.10：AE 导致的研究中断
**用户问题**: "有多少受试者因不良事件退出研究？"
**SQL**:
```sql
SELECT 
    dm.ARM,
    COUNT(DISTINCT ae.USUBJID) as withdrew_due_to_ae
FROM ae
INNER JOIN dm ON ae.USUBJID = dm.USUBJID
WHERE ae.AEACN LIKE '%DRUG WITHDRAWN%' 
   OR ae.AEACN LIKE '%WITHDRAWN%'
GROUP BY dm.ARM
```

---

## 3. 生命体征分析（VS 域）

### 示例 3.1：收缩压超过阈值
**用户问题**: "有多少次收缩压测量值超过 140 mmHg？"
**SQL**:
```sql
SELECT COUNT(*) as high_bp_count
FROM vs
WHERE VSTESTCD = 'SYSBP' AND VSSTRESN > 140
```

### 示例 3.2：基线生命体征
**用户问题**: "显示所有受试者的基线血压"
**SQL**:
```sql
SELECT 
    dm.USUBJID,
    dm.ARM,
    MAX(CASE WHEN vs.VSTESTCD = 'SYSBP' THEN vs.VSSTRESN END) as baseline_sysbp,
    MAX(CASE WHEN vs.VSTESTCD = 'DIABP' THEN vs.VSSTRESN END) as baseline_diabp
FROM dm
LEFT JOIN vs ON dm.USUBJID = vs.USUBJID AND vs.VSBLFL = 'Y'
WHERE vs.VSTESTCD IN ('SYSBP', 'DIABP')
GROUP BY dm.USUBJID, dm.ARM
```

### 示例 3.3：各访视的平均血压
**用户问题**: "各访视的平均收缩压和舒张压是多少？"
**SQL**:
```sql
SELECT 
    VISIT,
    AVG(CASE WHEN VSTESTCD = 'SYSBP' THEN VSSTRESN END) as mean_sysbp,
    AVG(CASE WHEN VSTESTCD = 'DIABP' THEN VSSTRESN END) as mean_diabp
FROM vs
WHERE VSTESTCD IN ('SYSBP', 'DIABP')
GROUP BY VISIT, VISITNUM
ORDER BY VISITNUM
```

### 示例 3.4：体重变化趋势
**用户问题**: "显示受试者的体重变化趋势"
**SQL**:
```sql
SELECT 
    vs.USUBJID,
    dm.ARM,
    vs.VISIT,
    vs.VSSTRESN as weight_kg,
    vs.VSSTRESN - FIRST_VALUE(vs.VSSTRESN) OVER (
        PARTITION BY vs.USUBJID 
        ORDER BY vs.VISITNUM
    ) as weight_change
FROM vs
INNER JOIN dm ON vs.USUBJID = dm.USUBJID
WHERE vs.VSTESTCD = 'WEIGHT'
ORDER BY vs.USUBJID, vs.VISITNUM
```

### 示例 3.5：异常生命体征
**用户问题**: "哪些受试者有异常的生命体征？"
**SQL**:
```sql
SELECT DISTINCT
    vs.USUBJID,
    dm.ARM,
    vs.VSTESTCD,
    vs.VSTEST,
    vs.VSSTRESN,
    vs.VSSTRESU,
    vs.VISIT
FROM vs
INNER JOIN dm ON vs.USUBJID = dm.USUBJID
WHERE 
    (vs.VSTESTCD = 'SYSBP' AND vs.VSSTRESN > 140) OR
    (vs.VSTESTCD = 'DIABP' AND vs.VSSTRESN > 90) OR
    (vs.VSTESTCD = 'PULSE' AND (vs.VSSTRESN < 60 OR vs.VSSTRESN > 100)) OR
    (vs.VSTESTCD = 'TEMP' AND (vs.VSSTRESN < 36.0 OR vs.VSSTRESN > 37.5))
ORDER BY vs.USUBJID, vs.VSTESTCD
```

---

## 4. 实验室检查分析（LB 域）

### 示例 4.1：肝功能异常
**用户问题**: "有多少受试者的 ALT 超过正常值上限的 3 倍？"
**SQL**:
```sql
SELECT 
    COUNT(DISTINCT USUBJID) as subjects_with_high_alt
FROM lb
WHERE LBTESTCD = 'ALT' 
  AND LBSTRESN > LBSTNRHI * 3
```

### 示例 4.2：异常实验室结果统计
**用户问题**: "各检查项目的异常率是多少？"
**SQL**:
```sql
SELECT 
    LBTESTCD,
    LBTEST,
    COUNT(*) as total_tests,
    SUM(CASE WHEN LBNRIND = 'ABNORMAL' THEN 1 ELSE 0 END) as abnormal_count,
    SUM(CASE WHEN LBNRIND = 'ABNORMAL' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as abnormal_rate
FROM lb
WHERE LBNRIND IS NOT NULL
GROUP BY LBTESTCD, LBTEST
HAVING COUNT(*) >= 10
ORDER BY abnormal_rate DESC
```

### 示例 4.3：血红蛋白基线与末次访视对比
**用户问题**: "对比受试者基线和末次访视的血红蛋白水平"
**SQL**:
```sql
SELECT 
    dm.USUBJID,
    dm.ARM,
    baseline.LBSTRESN as baseline_hgb,
    last_visit.LBSTRESN as last_hgb,
    last_visit.LBSTRESN - baseline.LBSTRESN as change_from_baseline
FROM dm
LEFT JOIN (
    SELECT USUBJID, LBSTRESN 
    FROM lb 
    WHERE LBTESTCD = 'HGB' AND LBBLFL = 'Y'
) baseline ON dm.USUBJID = baseline.USUBJID
LEFT JOIN (
    SELECT lb.USUBJID, lb.LBSTRESN
    FROM lb
    INNER JOIN (
        SELECT USUBJID, MAX(VISITNUM) as max_visit
        FROM lb
        WHERE LBTESTCD = 'HGB'
        GROUP BY USUBJID
    ) last ON lb.USUBJID = last.USUBJID AND lb.VISITNUM = last.max_visit
    WHERE lb.LBTESTCD = 'HGB'
) last_visit ON dm.USUBJID = last_visit.USUBJID
WHERE baseline.LBSTRESN IS NOT NULL
```

### 示例 4.4：肾功能评估
**用户问题**: "显示肌酐超过正常值的受试者"
**SQL**:
```sql
SELECT 
    dm.USUBJID,
    dm.AGE,
    dm.SEX,
    dm.ARM,
    lb.LBSTRESN as creatinine,
    lb.LBSTRESU as unit,
    lb.LBSTNRHI as upper_limit,
    lb.VISIT
FROM lb
INNER JOIN dm ON lb.USUBJID = dm.USUBJID
WHERE lb.LBTESTCD = 'CREAT' 
  AND lb.LBSTRESN > lb.LBSTNRHI
ORDER BY lb.LBSTRESN DESC
```

---

## 5. 综合分析（多域关联）

### 示例 5.1：有 SAE 且肝功能异常的受试者
**用户问题**: "找出既有严重不良事件又有肝功能异常的受试者"
**SQL**:
```sql
SELECT DISTINCT
    dm.USUBJID,
    dm.AGE,
    dm.SEX,
    dm.ARM,
    ae.AETERM as sae_term,
    lb.LBTEST as lab_test,
    lb.LBSTRESN as lab_value,
    lb.LBSTNRHI as upper_limit
FROM dm
INNER JOIN ae ON dm.USUBJID = ae.USUBJID AND ae.AESER = 'Y'
INNER JOIN lb ON dm.USUBJID = lb.USUBJID 
    AND lb.LBTESTCD IN ('ALT', 'AST')
    AND lb.LBSTRESN > lb.LBSTNRHI * 2
ORDER BY dm.USUBJID
```

### 示例 5.2：年龄>60 岁且有严重 AE 的受试者
**用户问题**: "显示年龄超过 60 岁且出现严重不良事件的受试者"
**SQL**:
```sql
SELECT DISTINCT
    dm.USUBJID,
    dm.AGE,
    dm.SEX,
    dm.ARM,
    ae.AETERM,
    ae.AESEV,
    ae.AESTDTC
FROM dm
INNER JOIN ae ON dm.USUBJID = ae.USUBJID
WHERE dm.AGE > 60 AND ae.AESER = 'Y'
ORDER BY dm.AGE DESC, ae.AESTDTC
```

### 示例 5.3：治疗组安全性综合对比
**用户问题**: "对比各治疗组的安全性指标"
**SQL**:
```sql
SELECT 
    dm.ARM,
    COUNT(DISTINCT dm.USUBJID) as total_subjects,
    COUNT(DISTINCT ae.USUBJID) as subjects_with_ae,
    COUNT(DISTINCT ae.USUBJID) * 100.0 / COUNT(DISTINCT dm.USUBJID) as ae_rate,
    COUNT(DISTINCT CASE WHEN ae.AESER = 'Y' THEN ae.USUBJID END) as subjects_with_sae,
    COUNT(DISTINCT CASE WHEN ae.AESER = 'Y' THEN ae.USUBJID END) * 100.0 / COUNT(DISTINCT dm.USUBJID) as sae_rate,
    SUM(CASE WHEN ae.AESER = 'Y' THEN 1 ELSE 0 END) as total_sae_events
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
GROUP BY dm.ARM
ORDER BY dm.ARM
```

### 示例 5.4：受试者完整安全性档案
**用户问题**: "生成受试者 'STUDY001-001-001' 的完整安全性报告"
**SQL**:
```sql
-- 基本信息
SELECT 
    dm.USUBJID,
    dm.AGE,
    dm.SEX,
    dm.RACE,
    dm.ARM,
    dm.RFSTDTC as study_start,
    dm.RFENDTC as study_end
FROM dm
WHERE dm.USUBJID = 'STUDY001-001-001'

UNION ALL

-- 不良事件
SELECT 
    'Adverse Event' as category,
    ae.AETERM as term,
    ae.AESEV as severity,
    ae.AESER as serious,
    ae.AEREL as relationship,
    ae.AESTDTC as start_date
FROM ae
WHERE ae.USUBJID = 'STUDY001-001-001'

UNION ALL

-- 异常实验室结果
SELECT 
    'Lab Abnormality' as category,
    lb.LBTEST as test,
    CAST(lb.LBSTRESN AS VARCHAR) as value,
    lb.LBSTRESU as unit,
    lb.LBNRIND as normal_flag,
    lb.LBDTC as test_date
FROM lb
WHERE lb.USUBJID = 'STUDY001-001-001'
  AND lb.LBNRIND IN ('ABNORMAL', 'HIGH', 'LOW')
```

---

## 6. 时间相关查询

### 示例 6.1：研究期间发生的 AE
**用户问题**: "显示研究治疗期间发生的所有不良事件"
**SQL**:
```sql
SELECT 
    ae.*
FROM ae
INNER JOIN dm ON ae.USUBJID = dm.USUBJID
WHERE ae.AESTDTC >= dm.RFSTDTC 
  AND ae.AESTDTC <= dm.RFENDTC
ORDER BY ae.AESTDTC
```

### 示例 6.2：首剂后 30 天内的 AE
**用户问题**: "统计首次用药后 30 天内发生的不良事件"
**SQL**:
```sql
SELECT 
    COUNT(*) as ae_count,
    COUNT(DISTINCT ae.USUBJID) as subject_count
FROM ae
INNER JOIN dm ON ae.USUBJID = dm.USUBJID
WHERE ae.AESTDTC >= dm.RFSTDTC
  AND ae.AESTDTC <= dm.RFSTDTC + INTERVAL '30' DAY
```

---

## 注意事项

1. **日期时间过滤**: 使用 `>= start_date AND < end_date + 1 day` 确保包含结束日期
2. **NULL 处理**: 使用 `IS NULL` 或 `IS NOT NULL` 而不是 `= NULL`
3. **DISTINCT 使用**: 统计受试者数时使用 `COUNT(DISTINCT USUBJID)`
4. **关联规则**: 所有域通过 `USUBJID` 与 DM 表关联
5. **控制术语**: 使用正确的控制术语值（如 AESER = 'Y' 而不是 'Yes'）
6. **百分比计算**: 使用 `* 100.0` 确保浮点运算
7. **排序**: 使用 `ORDER BY` 使结果更有意义

---

这些示例应作为 text2sql_prompt 的参考示例。
