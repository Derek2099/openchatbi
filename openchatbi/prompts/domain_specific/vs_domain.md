# VS Domain (Vital Signs) - 生命体征域

## 域概述
**用途**: 记录生命体征测量  
**特点**: 长格式存储（每次测量一条记录）  
**类型**: 发现域（Findings Domain）

---

## 核心变量

### 标识符变量
- **STUDYID** - 研究标识符
- **DOMAIN** - 域代码 ('VS')
- **USUBJID** - 唯一受试者ID
- **VSSEQ** - 生命体征序号

### 测试标识变量
- **VSTESTCD** - 测试代码（简短代码）
  - 'SYSBP' = 收缩压 (Systolic Blood Pressure)
  - 'DIABP' = 舒张压 (Diastolic Blood Pressure)
  - 'PULSE' = 脉搏/心率 (Pulse Rate)
  - 'TEMP' = 体温 (Temperature)
  - 'WEIGHT' = 体重 (Weight)
  - 'HEIGHT' = 身高 (Height)
  - 'RESP' = 呼吸率 (Respiratory Rate)
  - 'BMI' = 体质指数 (Body Mass Index)
- **VSTEST** - 测试名称（完整名称）

### 结果变量
- **VSORRES** - 原始结果（字符型，保留原始记录）
- **VSORRESU** - 原始结果单位
- **VSSTRESC** - 标准化结果（字符型）
- **VSSTRESN** - 标准化数值结果（用于统计分析）
- **VSSTRESU** - 标准化单位
  - 血压: mmHg
  - 体重: kg
  - 身高: cm
  - 体温: °C
  - 脉搏: beats/min

### 位置和条件变量
- **VSPOS** - 测量体位
  - 'SITTING' = 坐位
  - 'STANDING' = 站位
  - 'SUPINE' = 仰卧位
- **VSLAT** - 测量位置侧别（如左臂、右臂）

### 访视变量
- **VISIT** - 访视名称
- **VISITNUM** - 访视编号（数值）
- **VSDY** - 相对研究开始的天数

### 日期变量
- **VSDTC** - 测量日期时间（ISO 8601）

---

## 业务规则

1. **长格式**: 每次测量一条记录（不是宽格式）
2. **多重性**: 每个受试者在每次访视可有多个测量
3. **关联**: 通过 USUBJID 关联到 DM 域
4. **数值分析**: 使用 VSSTRESN（标准化数值）

---

## 常见查询模式

### 1. 收缩压基线值
```sql
SELECT 
    USUBJID,
    VSSTRESN as baseline_sysbp
FROM vs
WHERE VSTESTCD = 'SYSBP' 
  AND VISIT = 'Baseline'
```

### 2. 各访视收缩压平均值
```sql
SELECT 
    VISITNUM,
    VISIT,
    AVG(VSSTRESN) as mean_sysbp,
    STDDEV(VSSTRESN) as std_sysbp,
    COUNT(*) as n
FROM vs
WHERE VSTESTCD = 'SYSBP'
GROUP BY VISITNUM, VISIT
ORDER BY VISITNUM
```

### 3. 体重变化趋势
```sql
SELECT 
    USUBJID,
    VISITNUM,
    VSSTRESN as weight,
    VSSTRESN - FIRST_VALUE(VSSTRESN) OVER (PARTITION BY USUBJID ORDER BY VISITNUM) as weight_change
FROM vs
WHERE VSTESTCD = 'WEIGHT'
ORDER BY USUBJID, VISITNUM
```

### 4. 治疗组间血压对比
```sql
SELECT 
    dm.ARM,
    AVG(CASE WHEN vs.VSTESTCD='SYSBP' THEN vs.VSSTRESN END) as mean_sysbp,
    AVG(CASE WHEN vs.VSTESTCD='DIABP' THEN vs.VSSTRESN END) as mean_diabp
FROM dm
LEFT JOIN vs ON dm.USUBJID = vs.USUBJID
WHERE vs.VISIT = 'Week 12'
GROUP BY dm.ARM
```

### 5. 异常血压筛查
```sql
SELECT 
    vs.USUBJID,
    dm.ARM,
    vs.VISIT,
    vs.VSSTRESN as sysbp
FROM vs
INNER JOIN dm ON vs.USUBJID = dm.USUBJID
WHERE vs.VSTESTCD = 'SYSBP'
  AND (vs.VSSTRESN > 140 OR vs.VSSTRESN < 90)
ORDER BY vs.VSSTRESN DESC
```

### 6. BMI 计算（如果未直接记录）
```sql
SELECT 
    w.USUBJID,
    w.VISITNUM,
    w.VSSTRESN as weight_kg,
    h.VSSTRESN as height_cm,
    w.VSSTRESN / POWER(h.VSSTRESN / 100, 2) as calculated_bmi
FROM vs w
INNER JOIN vs h ON w.USUBJID = h.USUBJID 
               AND w.VISITNUM = h.VISITNUM
WHERE w.VSTESTCD = 'WEIGHT'
  AND h.VSTESTCD = 'HEIGHT'
```

### 7. 时间序列数据（用于预测）
```sql
SELECT 
    USUBJID,
    VSDTC as measurement_date,
    VSSTRESN as sysbp_value
FROM vs
WHERE VSTESTCD = 'SYSBP'
  AND USUBJID = 'STUDY001-001-001'
ORDER BY VSDTC
```

---

## 表选择规则

### 何时使用 VS 域
- ✅ 查询包含 "生命体征"、"vital signs"
- ✅ 查询 "血压"、"体重"、"体温"、"脉搏"
- ✅ 查询 "收缩压"、"舒张压"
- ✅ 查询特定访视的测量值
- ✅ 查询测量值的变化趋势

### 何时 JOIN DM 域
- ✅ 需要治疗组信息（ARM）
- ✅ 需要按治疗组分组分析
- ✅ 需要人口统计学信息

---

## SQL 生成注意事项

1. **测试代码**: 使用 VSTESTCD 过滤（如 'SYSBP', 'DIABP'）
2. **数值分析**: 使用 VSSTRESN（不是 VSORRES）
3. **访视过滤**: 可使用 VISIT 或 VISITNUM
4. **长格式**: 每个测试项一条记录，需要适当的过滤和聚合
5. **时间序列**: 按 VSDTC 或 VISITNUM 排序

---

## 时间序列预测支持

VS 域特别适合时间序列分析和预测：

```python
# 示例：收缩压预测
input_data = {
    "input_data": [
        {"date": "2024-01-01", "value": 120},
        {"date": "2024-01-08", "value": 122},
        {"date": "2024-01-15", "value": 118},
        # ... 至少 96 个数据点
    ],
    "forecast_window": 4,
    "frequency": "weekly"
}
```

---

## 数据质量检查

- ✅ USUBJID 存在于 DM
- ✅ VSTESTCD 值域检查
- ✅ VSSTRESN 合理范围
  - 收缩压: 80-200 mmHg
  - 舒张压: 40-120 mmHg
  - 体重: 30-200 kg
  - 体温: 35-42 °C
  - 脉搏: 40-200 beats/min
- ✅ 日期格式 ISO 8601
- ✅ 单位一致性
