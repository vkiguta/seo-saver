import styled, { keyframes } from 'styled-components';
import { Link as LinkRouter } from 'react-router-dom';

export const panelAnimation = keyframes`
from {
  opacity:0;
}
to {
  opacity:1;
}
`;

export const UserPanelContainer = styled.div`
  display: ${({ isOpen }) => (isOpen ? 'block' : 'none')};

  transition: all 0.5s linear;
  width: 280px;
  position: absolute;
  top: 51px;
  right: 0;

  animation: ${panelAnimation} 0.3s ease;

  border: 1px solid #e6e8f1;
  background-color: #fff;
  color: #686868;
  box-shadow: -10px 9px 21px rgba(128, 152, 213, 0.07);

  @media screen and (max-width: 768px) {
    width: 240px;
    display: flex;
    align-items: center;
    position: fixed;
    right: auto;
    top: 0;
    bottom: 0;
    left: ${({ isOpen }) => (isOpen ? 0 : '-240px')};
    width: 240px;
    transition: 0.3s ease;
    z-index: 16;
  }
`;
export const UserPanelWrapper = styled.div`
  padding: 32px 102px 10px 40px;
`;
export const UserHello = styled.div`
  height: 31px;
  width: 163px;
  font-size: 13px;
  text-align: left;
  border-bottom: 1px solid #e6e8f1;
`;
export const UserPanelList = styled.ul`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 115px;
  margin-top: 18px;
`;
export const UserPanelElement = styled.li`
  margin-bottom: 18px;
`;
export const UserPanelLink = styled(LinkRouter)`
  font-size: 13px;
  color: #686868;
  cursor: pointer;

  &:hover {
    color: #ffae00;
    transition: 0.3s ease;
  }
`;

export const UserPanelLinkExternal = styled.a`
  font-size: 13px;
  color: #686868;
  cursor: pointer;

  &:hover {
    color: #ffae00;
    transition: 0.3s ease;
  }
`;

export const UserPanelLogout = styled.button`
  padding: 0 !important;
  border: none;
  font-size: 13px;
  background: none !important;
  color: #686868;
  cursor: pointer;

  &:hover {
    color: #ffae00;
    transition: 0.3s ease;
  }
`;
