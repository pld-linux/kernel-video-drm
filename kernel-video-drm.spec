%define		_rel 3.1

Summary:	DRM drivers
Summary(pl):	Sterowniki DRM
Name:		kernel-video-drm
Version:	4.3.0
Release:        %{_rel}@%(echo %{__kernel_ver} | sed s/-/_/g)
License:	MIT
Group:		Base/kernel
Source0:	http://www.xfree86.org/~alanh/linux-drm-%{version}-kernelsource.tar.gz
URL:		http://www.xfree86.org/~alanh/
PreReq:		/sbin/depmod
PreReq:		modutils >= 2.3.18-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DRM drivers.

%description -l pl
Sterowniki DRM

%prep
%setup -q -n drm

%build
%{__make} -f Makefile.linux CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{__kernel_ver}/misc

install gamma.o tdfx.o r128.o radeon.o $RPM_BUILD_ROOT/lib/modules/%{__kernel_ver}/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc README.drm
/lib/modules/%{__kernel_ver}/misc/*
