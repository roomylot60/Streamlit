# Steamlit UI 생성

## 1. Container
- 영역을 설정해서 UI내 구역 구분
- 기본적인 container생성 코드

```python
container = st.continer()
```

- `key`값을 부여하여 container 별로 적용되는 css를 변경가능

```python
container1 = st.container(key="id_1")
```

```css
[data-testid='stContainer'][data-key="id_1"]{
    min-height: 400px;
    background-color: #00ff00;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}
```

## 2. Sidebar
- Streamlit은 기본적으로 Sidebar를 제공
- 기본적인 Sidebar의 형태

```python
with st.sidebar:
    st.title("Sidebar")
```


## 3. Input : st.write() / st.markdown()