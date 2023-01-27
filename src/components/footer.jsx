import { useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';

export default function AppFooter(){
    const [showTopBtn, setShowTopBtn] = useState(false);

    useEffect(()=>{
        window.addEventListener('scroll',()=>{
            if(window.scrollY >400){
                setShowTopBtn(true);
            }
            else{
                setShowTopBtn(false);
            }
        })

    },[])
    function goTop(){
        window.scrollTo({
            top:0,
            behavior:'smooth'
        })
    }

    return(
        <Container fluid>

            <div className="copyright">
                &copy; 2023 GCMC. All Right Reserved.
            </div>
            <div className="socials">
                <ul>
                    <li>
                        <a href ="#"> <i className="fab fa-facebook"></i></a>
                    </li>
                    <li>
                        <a href ="#"> <i className="fab fa-twitter"></i></a>
                    </li>
                    <li>
                        <a href ="#"> <i className="fab fa-linkedin-in"></i></a>
                    </li>
                </ul>
            </div>
            {showTopBtn && (<div className='go-top' onClick={goTop}></div>)}
            </Container>

    )
}