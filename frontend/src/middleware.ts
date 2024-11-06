import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtDecode } from 'jwt-decode';

export default async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('access_token');

  const publicPaths = ['/login', '/chat'];
  const isPublicPath = publicPaths.includes(pathname);

  if (!token && !isPublicPath) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (token) {
    const decodedToken: any = jwtDecode(token.value);
    const userRole = decodedToken.role;

    if (pathname === '/super-admin' && userRole !== 'super_admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url));
    }

    if (
      (pathname === '/users-dashboard' || pathname === '/company') &&
      userRole !== 'admin'
    ) {
      return NextResponse.redirect(new URL('/unauthorized', request.url));
    }

    if (pathname === '/company-details' && userRole !== 'operator') {
      return NextResponse.redirect(new URL('/unauthorized', request.url));
    
    }
    if (pathname === '/login') {
      let pathToRedirect = '/chat'
      switch (userRole) {
        case 'super_admin':
          pathToRedirect = '/super-admin';
          break;
        case 'admin':
          pathToRedirect = '/users-dashboard';
          break;
        case 'operator':
          pathToRedirect = '/company-details';
          break;
        default:
          pathToRedirect = '/chat';
      }
      return NextResponse.redirect(new URL(pathToRedirect, request.url));
    }
  }


  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
