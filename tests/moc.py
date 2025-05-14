# filepath: scripts/dump_mock_data.py
import json, asyncio
from httpx import AsyncClient

async def dump():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        out = {}
        # 1) получаем все семьи
        families = await client.get("/families")
        out["families"] = families.json()

        # 2) по каждой семье сохраняем пользователей и транзакции
        for fam in out["families"]:
            fid = fam["id"]
            out.setdefault("users", {})[fid] = (await client.get(f"/families/{fid}/users")).json()
            out.setdefault("transactions", {})[fid] = (await client.get(f"/families/{fid}/transactions")).json()

    # 3) в отдельный файл
    with open("mock_data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(dump())