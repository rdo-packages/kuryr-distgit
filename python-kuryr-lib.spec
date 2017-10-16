%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global project kuryr
%global library kuryr-lib
%global egg kuryr_lib

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name: python-%library
Version: XXX
Release: XXX
Summary: OpenStack Kuryr library
License:    ASL 2.0
URL:        http://docs.openstack.org/developer/kuryr

Source0:    https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz

BuildArch: noarch

%package -n python2-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python2-%{library}}


BuildRequires:  git
BuildRequires:  python-ddt
BuildRequires:  python2-devel
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-testtools
# Required for tests
BuildRequires:  python-keystoneauth1
BuildRequires:  python-neutronclient
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-utils
BuildRequires:  python-pyroute2

Requires:       python-ipaddress >= 1.0.7
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-neutronclient >= 6.3.0
Requires:       python-neutron-lib >= 1.9.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-pbr >= 2.0.0
Requires:       python-babel >= 2.3.4
Requires:       python-pyroute2 >= 0.4.15
Requires:       python-six >= 1.9.0

%description -n python2-%{library}
OpenStack Kuryr library shared by all Kuryr sub-projects.

%package -n python2-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python-%{library} = %{version}-%{release}
Requires:   python-ddt
Requires:   python-oslotest
Requires:   python-testtools

%description -n python2-%{library}-tests
OpenStack Kuryr library shared by all Kuryr sub-projects.

This package contains the Kuryr library test files.

%package doc
Summary:    OpenStack Kuryr library documentation

BuildRequires: python-sphinx
BuildRequires: python-reno
BuildRequires: python-openstackdocstheme

%description doc
OpenStack Kuryr library shared by all Kuryr sub-projects.

This package contains the documentation.

%package -n kuryr-binding-scripts
Summary:    OpenStack Kuryr binding scripts for SDNs

Requires: bash
Requires: iproute

%description -n kuryr-binding-scripts
OpenStack Kuryr library shared by all Kuryr sub-projects.

This package contains the binding scripts for different SDNs.


%if 0%{?with_python3}
%package -n python3-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  git
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
BuildRequires:  python3-pyroute2

Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-neutronclient >= 6.3.0
Requires:       python3-neutron-lib >= 1.9.0
Requires:       python3-oslo-concurrency >= 3.8.0
Requires:       python3-oslo-config >= 2:4.0.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-log >= 3.22.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-babel >= 2.3.4
Requires:       python3-pyroute2 >= 0.4.15
Requires:       python3-six >= 1.9.0

%description -n python3-%{library}
OpenStack Kuryr library shared by all Kuryr sub-projects

This package contains the Python3 version of the library

%package -n python3-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-ddt
Requires:   python3-oslotest
Requires:   python3-testtools

%description -n python3-%{library}-tests
OpenStack Kuryr library containing the tests for all Kuryr sub-projects

This package contains the Python3 version of the library tests.

%endif # with_python3


%description
OpenStack Kuryr library shared by all Kuryr sub-projects.

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f requirements.txt
rm -f test-requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{egg}-*.egg-info
%exclude %{python2_sitelib}/%{project}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{project}/tests

%files doc
%license LICENSE
%doc doc/build/html README.rst

%files -n kuryr-binding-scripts
%license LICENSE
%{_libexecdir}/kuryr

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{egg}-*.egg-info
%exclude %{python3_sitelib}/%{project}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{project}/tests
%endif

%changelog
