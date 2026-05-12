import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import AppleProvider from "next-auth/providers/apple";
import LinkedInProvider from "next-auth/providers/linkedin";
import AzureADProvider from "next-auth/providers/azure-ad"; // Outlook/Microsoft

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "placeholder_google_client_id",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "placeholder_google_client_secret",
    }),
    AppleProvider({
      clientId: process.env.APPLE_ID || "placeholder_apple_id",
      clientSecret: process.env.APPLE_SECRET || "placeholder_apple_secret",
    }),
    LinkedInProvider({
      clientId: process.env.LINKEDIN_CLIENT_ID || "placeholder_linkedin_client_id",
      clientSecret: process.env.LINKEDIN_CLIENT_SECRET || "placeholder_linkedin_client_secret",
      authorization: {
        params: { scope: 'openid profile email' },
      },
      issuer: 'https://www.linkedin.com',
      jwks_endpoint: 'https://www.linkedin.com/oauth/openid/jwks',
      profile(profile, tokens) {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
        };
      },
    }),
    AzureADProvider({
      clientId: process.env.AZURE_AD_CLIENT_ID || "placeholder_azure_client_id",
      clientSecret: process.env.AZURE_AD_CLIENT_SECRET || "placeholder_azure_client_secret",
      tenantId: process.env.AZURE_AD_TENANT_ID || "common",
    }),
  ],
  pages: {
    signIn: '/login', // Redirect to custom login page
  },
  callbacks: {
    async jwt({ token, account, user }) {
      // Persist the OAuth access_token to the token right after signin
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },
    async session({ session, token, user }) {
      // Send properties to the client, like an access_token from a provider.
      session.accessToken = token.accessToken;
      return session;
    }
  },
  secret: process.env.NEXTAUTH_SECRET || "placeholder_secret_for_development_only",
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
