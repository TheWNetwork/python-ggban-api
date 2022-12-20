# Python GGban API Wrapper


**Example:**

```
import asyncio
from ggban import Client


client = Client(id=12345678910, token="TOKEN HERE")


async def main():
    print("Get user:")
    user = await client.get_user(user_id=5513670669)
    print(f"Baneado: {user.ban} - Razon: {user.ban_reason}")
    print("Get report:")
    report = await client.get_report(report_id=32379)
    print(
        f"""
Usuario: {report.reported_id}
Fecha: {report.date}
Autor: {report.origin_id}
Estatus: {report.status}
Comentarios: {[com.__dict__ for com in report.comment]}
        """
    )
    print("Report test:")
    try:
        report_test = await client.new_report(user_id=1178259323, reported_id=5138672830, reason="TEST")
        print(f"Report ID: {report_test}")
    except Exception as error:
        print(error)


if __name__ == "__main__":
    asyncio.run(main())
```