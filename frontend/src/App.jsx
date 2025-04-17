import './App.css'
import { MainPage } from './pages/main-page.jsx'
import { Route,Routes } from 'react-router-dom'
import { AuthorizeForm } from './pages/auth/auth.jsx'

function App() {
 
  return (
    <div>
      <Routes>
      <Route path='/' element={<MainPage/>}/>
      <Route path='/auth' element={<AuthorizeForm/>}/>
      </Routes>
    </div>

  )
}

export default App