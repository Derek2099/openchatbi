# CDISC SDTM IG 3.4 域结构说明

## SDTM 数据仓库架构

SDTM (Study Data Tabulation Model) 是 CDISC 定义的临床试验数据标准化模型，用于统一临床试验数据的收集、存储和提交格式。

### 数据组织原则

1. **域（Domain）**: 数据按照功能和内容分类为不同的域
2. **观察类（Observation Class）**: 域分为多个观察类
   - **特殊用途域**: 人口统计学（DM）、批注（CO）等
   - **事件域**: 记录发生的事件（AE, MH, CE 等）
   - **干预域**: 记录治疗和用药（EX, CM 等）
   - **发现域**: 记录测量和观察结果（VS, LB, EG 等）
   - **试验设计域**: 研究设计信息（TA, TE, TV 等）
3. **关联**: 所有域通过 USUBJID（唯一受试者标识符）关联

---

## 核心域详解

### 1. DM - Demographics（人口统计学域）⭐ 核心域

**用途**: 存储受试者的基本信息

**特点**: 
- 每个受试者一条记录
- 所有其他域的关联基础
- 必需域

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('DM')
USUBJID     - 唯一受试者ID（格式: STUDYID-SITEID-SUBJID）
SUBJID      - 受试者编号
SITEID      - 研究中心ID
AGE         - 年龄（数值）
AGEU        - 年龄单位（通常为 'YEARS'）
SEX         - 性别（'M'=男性, 'F'=女性, 'U'=未知）
RACE        - 种族
ETHNIC      - 民族
COUNTRY     - 国家
ARM         - 计划治疗组名称
ARMCD       - 计划治疗组代码（如 'TRT', 'PLB'）
ACTARM      - 实际治疗组名称
ACTARMCD    - 实际治疗组代码
RFSTDTC     - 首次研究治疗日期
RFENDTC     - 最后研究治疗日期
RFXSTDTC    - 首次研究药物日期
RFXENDTC    - 最后研究药物日期
```

**示例查询**:
- "有多少名受试者参与了研究？" → `SELECT COUNT(*) FROM dm`
- "各治疗组的受试者数量" → `SELECT ARM, COUNT(*) FROM dm GROUP BY ARM`
- "年龄大于60岁的受试者" → `SELECT * FROM dm WHERE AGE > 60`

---

### 2. AE - Adverse Events（不良事件域）⭐ 高频使用

**用途**: 记录研究期间发生的所有不良事件

**特点**:
- 每个不良事件一条记录
- 一个受试者可以有多条 AE 记录
- 安全性分析的核心数据

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('AE')
USUBJID     - 唯一受试者ID
AESEQ       - AE 序列号
AETERM      - 报告的 AE 术语（报告者用语）
AEDECOD     - 标准化的 AE 术语（MedDRA 编码）
AECAT       - AE 类别
AESCAT      - AE 子类别
AESEV       - 严重程度（'MILD', 'MODERATE', 'SEVERE'）
AESER       - 严重 AE 标志（'Y'=是, 'N'=否）
AEREL       - 与研究药物的因果关系
            ('NOT RELATED', 'UNLIKELY RELATED', 
             'POSSIBLY RELATED', 'PROBABLY RELATED', 'RELATED')
AEACN       - 对研究药物采取的措施
AEOUT       - AE 结局
            ('RECOVERED/RESOLVED', 'RECOVERING/RESOLVING',
             'NOT RECOVERED/NOT RESOLVED', 'FATAL', 'UNKNOWN')
AESTDTC     - AE 开始日期时间
AEENDTC     - AE 结束日期时间
AESDTH      - 导致死亡（'Y'/'N'）
AESLIFE     - 危及生命（'Y'/'N'）
AESHOSP     - 导致/延长住院（'Y'/'N'）
```

**示例查询**:
- "严重不良事件有多少例？" → `SELECT COUNT(*) FROM ae WHERE AESER = 'Y'`
- "药物相关的 AE" → `SELECT * FROM ae WHERE AEREL IN ('POSSIBLY RELATED', 'RELATED')`
- "各治疗组的 AE 发生率" → 需要与 DM 表关联

---

### 3. VS - Vital Signs（生命体征域）

**用途**: 记录生命体征测量值

**特点**:
- 每次测量一条记录
- 包含多种生命体征类型
- 与访视关联

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('VS')
USUBJID     - 唯一受试者ID
VSSEQ       - VS 序列号
VSTESTCD    - 测试代码（'SYSBP', 'DIABP', 'PULSE', 'TEMP', 'WEIGHT', 'HEIGHT'）
VSTEST      - 测试名称
VSCAT       - 类别
VSORRES     - 原始结果（字符型）
VSORRESU    - 原始单位
VSSTRESN    - 标准化结果（数值型）
VSSTRESU    - 标准化单位
VSDTC       - 测量日期时间
VISITNUM    - 访视编号
VISIT       - 访视名称
VSBLFL      - 基线标志（'Y'=基线）
```

**常用 VSTESTCD 值**:
- `SYSBP`: Systolic Blood Pressure（收缩压）
- `DIABP`: Diastolic Blood Pressure（舒张压）
- `PULSE`: Pulse Rate（脉搏）
- `TEMP`: Temperature（体温）
- `WEIGHT`: Weight（体重）
- `HEIGHT`: Height（身高）
- `RESP`: Respiratory Rate（呼吸频率）
- `BMI`: Body Mass Index（体质指数）

**示例查询**:
- "显示所有收缩压测量" → `SELECT * FROM vs WHERE VSTESTCD = 'SYSBP'`
- "收缩压超过140的记录" → `SELECT * FROM vs WHERE VSTESTCD = 'SYSBP' AND VSSTRESN > 140`
- "基线体重" → `SELECT * FROM vs WHERE VSTESTCD = 'WEIGHT' AND VSBLFL = 'Y'`

---

### 4. LB - Laboratory（实验室检查域）

**用途**: 记录实验室检查结果

**特点**:
- 每次检查一条记录
- 包含血液学、生化、尿液等多种检查
- 包含正常值范围

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('LB')
USUBJID     - 唯一受试者ID
LBSEQ       - LB 序列号
LBTESTCD    - 检查代码（'ALT', 'AST', 'HGB', 'WBC'等）
LBTEST      - 检查名称
LBCAT       - 类别（'HEMATOLOGY', 'CHEMISTRY', 'URINALYSIS'）
LBSCAT      - 子类别
LBORRES     - 原始结果
LBORRESU    - 原始单位
LBSTRESN    - 标准化结果（数值）
LBSTRESU    - 标准化单位
LBSTNRLO    - 正常值下限
LBSTNRHI    - 正常值上限
LBNRIND     - 正常值标志（'NORMAL', 'ABNORMAL', 'HIGH', 'LOW'）
LBDTC       - 采样日期时间
VISITNUM    - 访视编号
VISIT       - 访视名称
LBBLFL      - 基线标志
```

**常用 LBTESTCD 示例**:
- 肝功能: `ALT`, `AST`, `BILI`, `ALP`
- 肾功能: `CREAT`, `BUN`, `UREA`
- 血液学: `HGB`, `WBC`, `PLT`, `RBC`
- 血糖: `GLUC`, `HBA1C`
- 血脂: `CHOL`, `TRIG`, `HDL`, `LDL`

**示例查询**:
- "ALT 超过正常值上限 3 倍" → `SELECT * FROM lb WHERE LBTESTCD = 'ALT' AND LBSTRESN > LBSTNRHI * 3`
- "异常的实验室结果" → `SELECT * FROM lb WHERE LBNRIND = 'ABNORMAL'`

---

### 5. EX - Exposure（暴露/用药域）

**用途**: 记录受试者对研究药物的暴露情况

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('EX')
USUBJID     - 唯一受试者ID
EXSEQ       - EX 序列号
EXTRT       - 治疗名称
EXDOSE      - 剂量
EXDOSU      - 剂量单位
EXDOSFRM    - 剂型
EXDOSFRQ    - 给药频率
EXROUTE     - 给药途径
EXSTDTC     - 开始日期时间
EXENDTC     - 结束日期时间
```

---

### 6. CM - Concomitant Medications（伴随用药域）

**用途**: 记录研究期间使用的其他药物

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('CM')
USUBJID     - 唯一受试者ID
CMSEQ       - CM 序列号
CMTRT       - 药物名称
CMDECOD     - 标准化药物名称（WHO Drug编码）
CMDOSE      - 剂量
CMDOSU      - 剂量单位
CMDOSFRQ    - 给药频率
CMROUTE     - 给药途径
CMSTDTC     - 开始日期时间
CMENDTC     - 结束日期时间
CMINDC      - 用药指征
```

---

### 7. DS - Disposition（处置域）

**用途**: 记录受试者的研究状态和处置

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('DS')
USUBJID     - 唯一受试者ID
DSSEQ       - DS 序列号
DSTERM      - 处置术语
DSDECOD     - 标准化处置术语
DSCAT       - 类别（'DISPOSITION EVENT', 'PROTOCOL MILESTONE'）
DSSTDTC     - 日期时间
DSDECOD     - 可能的值:
            'COMPLETED', 'SCREEN FAILURE', 'RANDOMIZED',
            'WITHDRAWN', 'ADVERSE EVENT', 'DEATH'
```

---

### 8. MH - Medical History（病史域）

**用途**: 记录受试者的既往病史

**核心变量**:
```
STUDYID     - 研究标识符
DOMAIN      - 域代码 ('MH')
USUBJID     - 唯一受试者ID
MHSEQ       - MH 序列号
MHTERM      - 病史术语
MHDECOD     - 标准化病史术语
MHCAT       - 类别
MHSTDTC     - 开始日期时间
MHENDTC     - 结束日期时间
```

---

## 域之间的关系

### 主关联关系
```
        DM (Demographics) [1对1基础]
         │
         ├─ USUBJID ──┐
         │            │
         ├────────────┼─→ AE (Adverse Events) [1对多]
         │            │
         ├────────────┼─→ VS (Vital Signs) [1对多]
         │            │
         ├────────────┼─→ LB (Laboratory) [1对多]
         │            │
         ├────────────┼─→ EX (Exposure) [1对多]
         │            │
         ├────────────┼─→ CM (Concomitant Meds) [1对多]
         │            │
         ├────────────┼─→ MH (Medical History) [1对多]
         │            │
         └────────────┴─→ DS (Disposition) [1对多]
```

### 关联规则
1. **必须通过 USUBJID 关联**: 所有域表都通过 USUBJID 与 DM 表关联
2. **DM 表是基础**: 查询其他域时通常需要与 DM 表 JOIN 以获取治疗组、人口统计学信息
3. **时间关联**: 可通过日期时间变量（--STDTC, --ENDTC）进行时间范围过滤
4. **访视关联**: VS, LB 等域可通过 VISITNUM 或 VISIT 关联到访视

---

## 常见查询模式

### 1. 单域查询
```sql
-- 示例：查询所有严重 AE
SELECT * FROM ae WHERE AESER = 'Y'
```

### 2. 与 DM 关联查询（获取治疗组信息）
```sql
-- 示例：各治疗组的 AE 发生率
SELECT 
    dm.ARM,
    COUNT(DISTINCT ae.USUBJID) * 100.0 / COUNT(DISTINCT dm.USUBJID) as ae_rate
FROM dm
LEFT JOIN ae ON dm.USUBJID = ae.USUBJID
GROUP BY dm.ARM
```

### 3. 多域关联查询
```sql
-- 示例：有严重 AE 且肝功能异常的受试者
SELECT DISTINCT dm.USUBJID, dm.AGE, dm.SEX, dm.ARM
FROM dm
INNER JOIN ae ON dm.USUBJID = ae.USUBJID AND ae.AESER = 'Y'
INNER JOIN lb ON dm.USUBJID = lb.USUBJID 
    AND lb.LBTESTCD = 'ALT' 
    AND lb.LBSTRESN > lb.LBSTNRHI * 3
```

### 4. 时间范围查询
```sql
-- 示例：研究前30天内的 AE
SELECT * FROM ae
WHERE AESTDTC >= dm.RFSTDTC - INTERVAL '30' DAY
AND AESTDTC <= dm.RFENDTC
```

---

## SDTM 特定规则

### 1. 命名约定
- 域代码: 2个字符，大写（DM, AE, VS 等）
- 变量名: 大写，前缀为域代码（AETERM, VSTEST 等）
- 测试代码（--TESTCD）: 最多 8 个字符

### 2. 日期时间格式
- ISO 8601 格式: `YYYY-MM-DDTHH:MM:SS`
- 部分日期允许: `2024-01`, `2024`
- 时区可选: `2024-01-15T10:30:00-05:00`

### 3. 控制术语（Controlled Terminology）
- 某些变量有预定义的允许值
- 示例: SEX ('M', 'F', 'U'), AESER ('Y', 'N')

### 4. 基线标志（--BLFL）
- 标识基线测量: `'Y'` = 基线, 空 = 非基线
- 用于 VS, LB 等域

---

此文档应作为 schema_linking 和 text2sql 提示词的数据仓库介绍部分。
