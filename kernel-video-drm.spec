#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
# TODO: UP/SMP
%define		_rel 3.1

Summary:	DRM drivers
Summary(pl):	Sterowniki DRM
Name:		kernel-video-drm
Version:	4.3.0
Release:	%{_rel}@%{_kernel_ver_str}
License:	MIT
Group:		Base/kernel
Source0:	http://www.xfree86.org/~alanh/linux-drm-%{version}-kernelsource.tar.gz
# Source0-md5:	34515784c7b67f6cc9169aa9eed982c7
URL:		http://www.xfree86.org/~alanh/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,postun):		/sbin/depmod
Requires(post,postun):		modutils >= 2.3.18-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DRM drivers.

%description -l pl
Sterowniki DRM.

%prep
%setup -q -n drm

%build
%{__make} -f Makefile.linux CFLAGS="%{rpmcflags}" VERSION=%{_kernel_ver}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

install gamma.o tdfx.o r128.o radeon.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc README.drm
/lib/modules/%{_kernel_ver}/misc/*
