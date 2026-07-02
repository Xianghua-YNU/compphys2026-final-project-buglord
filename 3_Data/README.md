# 3_Data/ - 模拟与公开数据目录

目的: 存放模拟过程中产生的数据或用于分析的外部公开数据。该目录包含一个用于演示的小型 Pantheon 子集（微缩样本），以及说明如何获取和处理完整公开数据集（Pantheon、JLA、Union）。

管理原则
- 按需存放: 若模拟生成的数据量较小（如几百 KB 的 CSV/JSON），建议上传以方便复现结果。我们在此保留了一个小型演示样本 `processed_data/pantheon_sample.csv`（<<50KB）。
- 大文件禁令: 若单个数据文件超过 50MB，请勿上传至 GitHub。请使用数据获取脚本（见 2_Code/scripts/fetch_and_prepare_pantheon.py）在本地或 CI 环境下载并处理完整数据集。
- 公开数据: 若项目基于天文学公开数据集，建议在此存放“微缩采样版”供演示使用。本仓库包含微缩样本用于演示管线工作流程。

目录说明
- `raw_data/` (可选): 存放原始下载的数据（建议不要上传大文件）。
- `processed_data/`: 存放可直接用于分析的轻量化 CSV（如本仓库示例）。

如何重现或获取完整 Pantheon 数据
1) 我们提供了一个数据准备脚本位于 `2_Code/scripts/fetch_and_prepare_pantheon.py`，它可以：
   - 直接使用 Pantheon 原始文件（`lcparam_full_long.txt`）中的预计算 MU/dMU（若存在）；或
   - 在原始文件只包含光变曲线输出（`mb`, `x1`, `color` 等）时，使用给定的 nuisance 参数（`--alpha`, `--beta`, `--M`, `--sigma_int`）计算距离模数并估计误差。

2) 运行示例（在仓库根目录下）：
   ```bash
   python 2_Code/scripts/fetch_and_prepare_pantheon.py \
     --url https://raw.githubusercontent.com/dscolnic/Pantheon/master/lcparam_full_long.txt \
     --out 3_Data/processed_data/pantheon_sn.csv
   ```
   然后使用分析脚本：
   ```bash
   python 2_Code/run_all.py --data 3_Data/processed_data/pantheon_sn.csv --quick
   ```

注意事项
- 若你需要完整的 Pantheon+（更新版），请参阅 https://github.com/PantheonPlusSH0ES/DataRelease 并按其数据说明处理。不同发布的列名和内容可能不同，`fetch_and_prepare_pantheon.py` 提供了基本的自动处理逻辑，但在必要时可能需要针对具体数据发布做小修改。
- 若在 CI（GitHub Actions）中运行，请确保仓库设置允许 Actions 在成功后将生成的输出推回主分支（本仓库包含一个示例 workflow）。

演示样本
- `processed_data/pantheon_sample.csv`：一个微缩的示例数据集（用于快速本地测试与演示）。
