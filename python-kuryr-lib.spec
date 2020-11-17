%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global project kuryr
%global library kuryr-lib
%global egg kuryr_lib

%global common_desc OpenStack Kuryr library shared by all Kuryr sub-projects.

Name: python-%library
Version: XXX
Release: XXX
Summary: OpenStack Kuryr library
License:    ASL 2.0
URL:        http://docs.openstack.org/developer/kuryr

Source0:    https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%package -n python3-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python3-%{library}}


BuildRequires:  python3-ddt
BuildRequires:  python3-devel
BuildRequires:  python3-oslotest
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-testtools
# Required for tests
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-neutronclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-upgradecheck
BuildRequires:  python3-pyroute2

Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-neutron-lib >= 1.13.0
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-upgradecheck >= 0.1.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-babel >= 2.3.4
Requires:       python3-pyroute2 >= 0.5.6


%description -n python3-%{library}
%{common_desc}

%package -n python3-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-ddt
Requires:   python3-oslotest
Requires:   python3-testtools

%description -n python3-%{library}-tests
%{common_desc}

This package contains the Kuryr library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Kuryr library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-reno
BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%package -n kuryr-binding-scripts
Summary:    OpenStack Kuryr binding scripts for SDNs

Requires: bash
Requires: iproute

%description -n kuryr-binding-scripts
%{common_desc}

This package contains the binding scripts for different SDNs.

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
%{__python3} setup.py test

%files -n python3-%{library}
%license LICENSE
%{_bindir}/%{project}-status
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{egg}-*.egg-info
%exclude %{python3_sitelib}/%{project}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{project}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n kuryr-binding-scripts
%license LICENSE
%{_libexecdir}/kuryr

%changelog
