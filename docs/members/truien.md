# truien — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm (kèm link commit):**
  - Hoàn thiện vòng đời khách, giữ chỗ, bếp, phục vụ, tip và HUD trong Phase 1 (các commit `103de11`, `6b0aaac`, `174cbff`, `ac04145`, `c0ceefd`, `49b909e`, `ee8e33a`).
  - Viết bộ test `tests/test_quan_p1.py`, rà soát các ca biên trong Phase 2 và Phase 3.
  - Phụ trách vai trò PO & QA Lead: ghi chép `docs/clarify.md`, ma trận nghiệm thu `docs/verification/` qua cả 4 phase, điều phối Retro nhóm.
- **Tôi đã review (kèm link):**
  - Review module `chonoi/sim/gather.py`, `tests/test_gather.py` và các Agent skills của teammate `minh17023`.
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI sinh code lúc đầu chưa xử lý triệt để trường hợp scenario đưa vào khách không có món yêu cầu. Tôi phát hiện khi chạy headless bị fail và bổ sung logic gán món mặc định hợp lệ.
- **Điều tôi học được:**
  - Thiết kế event-driven và snapshot tất định giúp tách rời hoàn toàn tầng mô phỏng và tầng hiển thị, đảm bảo chất lượng kiểm thử tự động.
