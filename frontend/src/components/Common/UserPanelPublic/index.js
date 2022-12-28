import {
  UserPanelPublicContainer,
  UserPanelPublicWrapper,
  UserHelloPublic,
  UserPanelPublicList,
  UserPanelPublicElement,
  UserPanelPublicLink,
  UserPanelLinkExternalPublic,
} from './UserPanelPublicElements';

const UserPanelPublic = ({ isOpen, setIsOpen }) => {
  return (
    <>
      <UserPanelPublicContainer
        onClick={() => setIsOpen(!isOpen)}
        isOpen={isOpen}>
        <UserPanelPublicWrapper>
          <UserHelloPublic>Hello!</UserHelloPublic>
          <UserPanelPublicList>
            <UserPanelPublicElement>
              <UserPanelPublicLink to='/login' style={{ color: '#ffae00' }}>
                Login
              </UserPanelPublicLink>
            </UserPanelPublicElement>
            <UserPanelPublicElement>
              <UserPanelPublicLink to='/register' style={{ color: '#ffae00' }}>
                Register
              </UserPanelPublicLink>
            </UserPanelPublicElement>
            <UserPanelPublicElement>
              <UserPanelPublicLink to='/about'>About us</UserPanelPublicLink>
            </UserPanelPublicElement>
            <UserPanelPublicElement>
              <UserPanelPublicLink to='/support'>
                Support us
              </UserPanelPublicLink>
            </UserPanelPublicElement>
            <UserPanelPublicElement>
              <UserPanelPublicLink to='/news'>News</UserPanelPublicLink>
            </UserPanelPublicElement>
            <UserPanelPublicElement>
              <UserPanelLinkExternalPublic
                href='https://github.com/vkiguta/seo-saver'
                target='_blank'>
                Helpdesk / Github
              </UserPanelLinkExternalPublic>
            </UserPanelPublicElement>
          </UserPanelPublicList>
        </UserPanelPublicWrapper>
      </UserPanelPublicContainer>
    </>
  );
};

export default UserPanelPublic;
