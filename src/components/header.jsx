import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Image from 'react-bootstrap/Image'
import logo from '../assets/images/logo.png';



export default function AppHeader(){

    return (
        <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand href="#home">
        
        <Image className="logo" src= {logo} />
        
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
            <Nav.Link href="#services">Our Work</Nav.Link>
            <Nav.Link href="#works">Gallery</Nav.Link>
            <Nav.Link href="#contact">Contact Us</Nav.Link>
          
            
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    )
    
    }