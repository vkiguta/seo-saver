import {
  FooterContainer,
  FooterWrapper,
  FooterTitle,
  FooterLinkWrap,
  FooterLink,
} from './FooterElements';

const Footer = () => {
  return (
    <>
      <FooterContainer>
        <FooterWrapper>
          <FooterTitle>Have an idea?</FooterTitle>
          <FooterLinkWrap>
            <FooterLink
              href='https://github.com/vkiguta/seo-saver'
              target='_blank'>
              Send message
            </FooterLink>
          </FooterLinkWrap>
        </FooterWrapper>
      </FooterContainer>
    </>
  );
};

export default Footer;
