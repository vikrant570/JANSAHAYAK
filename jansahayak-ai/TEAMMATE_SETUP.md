\# JanSahayak Backend Setup



\## Requirements



Python 3.12.x is recommended.



\## 1. Clone



```bash

git clone https://github.com/shwetasingh199/jansahayak-ai

cd jansahayak-ai

```



\## 2. Virtual environment



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\## 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\## 4. Environment



```powershell

Copy-Item .env.example .env

```



Add the required API credentials privately.



\## 5. Start backend



```powershell

uvicorn app.main:app --reload

```



\## 6. Test



Health:



```text

http://127.0.0.1:8000/api/v1/health

```



Swagger:



```text

http://127.0.0.1:8000/docs

```



Chat:



```text

POST http://127.0.0.1:8000/api/v1/chat

```



\## 7. Next.js



Use:



```env

NEXT\_PUBLIC\_API\_BASE\_URL=http://127.0.0.1:8000

```



The frontend should render:



```typescript

data.answer

```



using `react-markdown`.

